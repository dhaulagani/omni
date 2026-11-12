"""Monitor upstream GitHub repositories for absorbed OMNI skills and auto-update when behind."""

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import absorb


def normalize_repo_url(url):
    """Return canonical HTTPS GitHub URL without trailing slash or .git suffix."""
    return re.sub(r"\.git$", "", str(url).strip().rstrip("/"))


def collect_upstreams(reg):
    """Group adapters by canonical upstream repository URL."""
    upstreams = {}
    for name, data in reg.get("adapters", {}).items():
        raw_url = data.get("upstream_url") or (
            data.get("source") if str(data.get("source", "")).startswith("http") else ""
        )
        if not raw_url:
            continue
        url = normalize_repo_url(raw_url)
        group = upstreams.setdefault(url, {
            "url": url,
            "author": data.get("author") or url.split("github.com/")[-1].split("/")[0],
            "stored_commit": "",
            "adapters": [],
        })
        group["adapters"].append(name)
        if not group["stored_commit"] and data.get("upstream_commit"):
            group["stored_commit"] = data["upstream_commit"]
    return upstreams


def fetch_remote_head(repo_url, timeout=15):
    """Resolve remote HEAD commit SHA via git ls-remote without cloning."""
    git_url = repo_url if repo_url.endswith(".git") else f"{repo_url}.git"
    try:
        res = subprocess.run(
            ["git", "ls-remote", git_url, "HEAD"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip().split()[0]
    except Exception:
        pass
    return None


def _evaluate_one(url, info, fetcher):
    remote_sha = fetcher(url)
    stored_sha = info["stored_commit"]
    if not remote_sha:
        status = "ERROR"
    elif not stored_sha:
        status = "UNTRACKED_COMMIT"
    elif remote_sha == stored_sha:
        status = "UP_TO_DATE"
    else:
        status = "UPDATE_AVAILABLE"
    return {
        "url": url,
        "author": info["author"],
        "stored_commit": stored_sha,
        "remote_commit": remote_sha or "",
        "status": status,
        "adapter_count": len(info["adapters"]),
        "adapters": sorted(info["adapters"]),
    }


def run_monitor(auto_update=False, sync=True, fetcher=fetch_remote_head, updater=None, syncer=None):
    """Check all upstream GitHub sources and optionally re-absorb updated repositories."""
    reg = absorb.load_registry()
    upstreams = collect_upstreams(reg)
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(_evaluate_one, url, info, fetcher): url
            for url, info in sorted(upstreams.items())
        }
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())

    results.sort(key=lambda r: r["url"].lower())
    now_ts = int(datetime.now().timestamp())
    for item in results:
        for name in item["adapters"]:
            if name in reg.get("adapters", {}):
                reg["adapters"][name]["last_checked"] = now_ts
    absorb.save_registry(reg)

    updated_any = False
    if auto_update:
        do_absorb = updater or absorb.absorb_source
        for item in results:
            if item["status"] in ("UPDATE_AVAILABLE", "UNTRACKED_COMMIT"):
                print(f"[*] Auto-updating from {item['url']} ({item['status']})...")
                if do_absorb(item["url"], sync=False):
                    updated_any = True

    if updated_any and sync:
        do_sync = syncer or absorb.sync_to_cluster
        do_sync()

    return results


def _print_report(results):
    print("\n=== OMNI Upstream Monitor Report ===")
    for r in results:
        old_s = r["stored_commit"][:12] or "none"
        new_s = r["remote_commit"][:12] or "unreachable"
        print(f"  [{r['status']:17s}] {r['url']} ({r['adapter_count']} adapters) | {old_s} -> {new_s}")
    updates = [r for r in results if r["status"] in ("UPDATE_AVAILABLE", "UNTRACKED_COMMIT")]
    print(f"\nChecked {len(results)} upstream repos. Updates pending: {len(updates)}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor upstream GitHub repos for OMNI adapters.")
    parser.add_argument("--auto-update", action="store_true", help="Re-absorb repositories with upstream updates.")
    parser.add_argument("--no-sync", action="store_true", help="Skip cluster sync after auto-update.")
    parser.add_argument("--json", action="store_true", help="Output JSON report.")
    args = parser.parse_args()

    res = run_monitor(auto_update=args.auto_update, sync=not args.no_sync)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        _print_report(res)
