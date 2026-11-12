# OMNI Capability Adapter: git-data-api
> Origin: core_skills (~\.gemini\config\skills\git-data-api\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: DISTINCT_CAPABILITY (Related: agent-reach, Sim: 3%)
> Categories: Code Minimization & Pragmatism, Frontend & Human Design, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning

# Zero-Disk-Bloat Git Data API Engine

Designed specifically for operating on massive repositories (such as monorepos > 500MB - 2GB+ like `BasedHardware/omi`) where local git cloning is slow, disk-heavy, and unviable on resource-constrained environments.

---

## 1. Algorithmic Workflow (0-Clone PR Creation)

```
Upstream Repo (main) ──> [1. GET /git/ref/heads/main] ──> Base Commit SHA
                                                               │
                                                               ▼
[2. GET /git/commits/{base_sha}] ──────────────────────> Base Tree SHA
                                                               │
                                                               ▼
[3. POST /git/blobs] (Send edited file contents) ───────> New Blob SHAs
                                                               │
                                                               ▼
[4. POST /git/trees] (base_tree + path-mode-blob array) ─> New Tree SHA
                                                               │
                                                               ▼
[5. POST /git/commits] (tree_sha + parent [base_sha]) ──> New Commit SHA
                                                               │
                                                               ▼
[6. POST/PATCH /git/refs/heads/{branch}] ───────────────> Branch Created/Updated
                                                               │
                                                               ▼
[7. POST /pulls] (head: fork:branch, base: main) ────────> PR Opened!
```

---

## 2. Python Reference Implementation

```python
import json
import urllib.request

TOKEN = "gho_..."
HEADERS = {
    "User-Agent": "GitHubCLI/2.46.0",
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def gh_api(url, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(f"https://api.github.com{url}", data=body, headers=HEADERS, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def submit_hermetic_pr(upstream_owner, upstream_repo, fork_owner, branch_name, file_changes, pr_title, pr_body):
    # 1. Base commit & tree
    ref = gh_api(f"/repos/{upstream_owner}/{upstream_repo}/git/ref/heads/main")
    base_sha = ref["object"]["sha"]
    base_tree_sha = gh_api(f"/repos/{upstream_owner}/{upstream_repo}/git/commits/{base_sha}")["tree"]["sha"]

    # 2. Build tree entries
    tree_items = []
    for path, content in file_changes.items():
        blob = gh_api(f"/repos/{fork_owner}/{upstream_repo}/git/blobs", method="POST", payload={"content": content, "encoding": "utf-8"})
        tree_items.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

    # 3. Create tree & commit
    new_tree = gh_api(f"/repos/{fork_owner}/{upstream_repo}/git/trees", method="POST", payload={"base_tree": base_tree_sha, "tree": tree_items})
    new_commit = gh_api(f"/repos/{fork_owner}/{upstream_repo}/git/commits", method="POST", payload={
        "message": pr_title,
        "tree": new_tree["sha"],
        "parents": [base_sha]
    })

    # 4. Create/update branch ref
    try:
        gh_api(f"/repos/{fork_owner}/{upstream_repo}/git/refs", method="POST", payload={"ref": f"refs/heads/{branch_name}", "sha": new_commit["sha"]})
    except Exception:
        gh_api(f"/repos/{fork_owner}/{upstream_repo}/git/refs/heads/{branch_name}", method="PATCH", payload={"sha": new_commit["sha"], "force": True})

    # 5. Open Pull Request
    return gh_api(f"/repos/{upstream_owner}/{upstream_repo}/pulls", method="POST", payload={
        "title": pr_title,
        "head": f"{fork_owner}:{branch_name}",
        "base": "main",
        "body": pr_body
    })
```

---

## 3. Best Practices
* Always fetch upstream `base_sha` immediately before creating the tree to prevent fast-forward divergence.
* Ensure all files are linted or formatted (e.g. `black`) BEFORE calculating blob SHAs.
* Use `utf-8` encoding exclusively in blob creation payloads.
