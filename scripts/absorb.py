import sys
import os
import json
import shutil
import subprocess
import tempfile
import re
import tarfile
from datetime import datetime

OMNI_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADAPTERS_DIR = os.path.join(OMNI_DIR, "adapters")
REFERENCES_DIR = os.path.join(OMNI_DIR, "references")
SCRIPTS_DIR = os.path.join(OMNI_DIR, "scripts")
REGISTRY_PATH = os.path.join(OMNI_DIR, "registry.json")
HISTORY_MD_PATH = os.path.join(OMNI_DIR, "ABSORPTION_HISTORY.md")
GLOBAL_NODES_CONFIG = os.path.join(os.path.expanduser("~"), ".gemini", "config", "omni-nodes.json")

IGNORED_DIRS = {".git", "tests", "test", "fixtures", "__pycache__", "node_modules", ".venv", "venv"}
PROTECTED_SCRIPTS = {"absorb.py", "monitor.py"}

os.makedirs(ADAPTERS_DIR, exist_ok=True)
os.makedirs(REFERENCES_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True)

CATEGORIES_KEYWORDS = {
    "Code Minimization & Pragmatism": ["yagni", "lazy", "minimal", "minimalist", "ponytail", "bloat", "diff", "short"],
    "Testing & Quality Assurance": ["test", "tdd", "red-green-refactor", "unit", "pytest", "mock", "fixture", "coverage"],
    "Debugging & Root Cause": ["debug", "systematic", "root-cause", "diagnos", "trace", "stack", "error", "troubleshoot"],
    "Frontend & Human Design": ["ui", "visual", "design", "antislop", "contrast", "wcag", "css", "layout", "mobile", "a11y"],
    "Memory & Knowledge Continuity": ["memory", "palace", "recall", "obsidian", "vault", "adr", "journal", "diary", "log"],
    "AST & Code Intelligence": ["ast", "tree-sitter", "codegraph", "blast-radius", "callgraph", "mue", "refactor"],
    "Reverse Engineering & Inspection": ["reverse", "decompile", "apk", "binary", "craft", "inspect", "disassemble"]
}

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "1.1.0",
        "last_updated": int(datetime.now().timestamp()),
        "adapters": {}
    }

def save_registry(reg):
    reg["last_updated"] = int(datetime.now().timestamp())
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)

def extract_tokens(text):
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    stop_words = {"the", "and", "for", "with", "that", "this", "from", "use", "when", "any", "you", "are", "code"}
    return set(w for w in words if w not in stop_words)

def classify_capability(text):
    text_lower = text.lower()
    matched_cats = []
    for cat, kws in CATEGORIES_KEYWORDS.items():
        if any(kw in text_lower for kw in kws):
            matched_cats.append(cat)
    return matched_cats if matched_cats else ["General Engineering"]

def calculate_similarity(tokens1, tokens2):
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return round(len(intersection) / len(union), 3)

def evaluate_novelty(skill_name, body_text, reg):
    new_tokens = extract_tokens(skill_name + " " + body_text[:2000])
    categories = classify_capability(skill_name + " " + body_text)
    
    highest_sim = 0.0
    most_similar_skill = None

    for existing_name, data in reg.get("adapters", {}).items():
        if existing_name == skill_name:
            return "EXACT_REVISION", existing_name, 1.0, categories
        
        exist_tokens = set(data.get("tokens", []))
        if not exist_tokens:
            exist_desc = data.get("description", "")
            exist_tokens = extract_tokens(existing_name + " " + exist_desc)
        
        sim = calculate_similarity(new_tokens, exist_tokens)
        if sim > highest_sim:
            highest_sim = sim
            most_similar_skill = existing_name

    if highest_sim >= 0.45:
        relation = "SIMILAR_EXTENSION"
    elif highest_sim >= 0.20:
        relation = "PARTIAL_OVERLAP"
    else:
        relation = "BRAND_NEW_CAPABILITY"

    return relation, most_similar_skill, highest_sim, categories

def generate_markdown_history(reg):
    adapters = reg.get("adapters", {})
    total = len(adapters)
    
    # Group verified upstream credits
    upstreams = {}
    for name, data in adapters.items():
        u_url = data.get("upstream_url") or (data.get("source") if str(data.get("source", "")).startswith("http") else "")
        if not u_url:
            continue
        grp = upstreams.setdefault(u_url, {
            "author": data.get("author") or u_url.split("github.com/")[-1].split("/")[0],
            "commit": data.get("upstream_commit", ""),
            "count": 0,
        })
        grp["count"] += 1
        if not grp["commit"] and data.get("upstream_commit"):
            grp["commit"] = data["upstream_commit"]

    lines = [
        "# 🧭 OMNI Capability Registry & Absorption History",
        "",
        "> Official registry of all capabilities and skills absorbed into the OMNI Kernel.",
        f"> Last updated: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC+7')}** | Total Capabilities: **{total} Adapters**",
        "",
        "---",
        "",
        "## 1. Upstream Credits & Attribution",
        "",
        "| Upstream Repository | Author / Maintainer | Absorbed Skills | Tracked Commit |",
        "|---|---|---|---|"
    ]

    for u_url in sorted(upstreams.keys(), key=str.lower):
        info = upstreams[u_url]
        repo_slug = u_url.split("github.com/")[-1].rstrip("/")
        sha_short = f"`{info['commit'][:12]}`" if info["commit"] else "`untracked`"
        lines.append(f"| [{repo_slug}]({u_url}) | {info['author']} | {info['count']} | {sha_short} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Absorbed Capability Matrix",
        "",
        "| No | Skill / Adapter | Primary Categories | Relation Status | Similarity / Related To | Upstream / Source |",
        "|---|---|---|---|---|---|"
    ])

    for idx, (name, data) in enumerate(sorted(adapters.items()), 1):
        rel = data.get("relation", "ACTIVE")
        sim_target = data.get("similar_to")
        sim_pct = int(data.get("similarity_score", 0) * 100)
        sim_info = f"`{sim_target}` ({sim_pct}%)" if sim_target else "Unique Novel"
        cats = ", ".join(data.get("categories", ["General"]))
        u_url = data.get("upstream_url", "")
        src = u_url or data.get("source", "local")
        if "github.com" in src:
            src_display = f"[{src.split('github.com/')[-1]}]({src})"
        elif data.get("author"):
            src_display = f"{data['author']} (`{os.path.basename(src)}`)"
        else:
            src_display = f"`{os.path.basename(src)}`"

        lines.append(f"| {idx} | **`{name}`** | {cats} | `{rel}` | {sim_info} | {src_display} |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Duplication Detection & Novelty Assessment",
        "",
        "OMNI uses Jaccard token analysis and domain extraction to classify every absorbed skill into three tiers:",
        "1. **`BRAND_NEW_CAPABILITY` (Score < 20%):** Introduces a distinct domain capability, expanding OMNI into new territory.",
        "2. **`SIMILAR_EXTENSION` / `PARTIAL_OVERLAP` (Score 20% - 70%):** Complements an existing capability without overwriting it; stored as a specialized adapter.",
        "3. **`EXACT_REVISION` (Score > 70% / Identical):** Version update or revision of an existing absorbed skill.",
        "",
        "---",
        "",
        "## 4. Technical Details Per Adapter",
        ""
    ])

    for name, data in sorted(adapters.items()):
        lines.append(f"### 📦 `{name}`")
        lines.append(f"- **Description:** {data.get('description', '-')}")
        lines.append(f"- **Categories:** {', '.join(data.get('categories', []))}")
        lines.append(f"- **Relation:** `{data.get('relation', 'ACTIVE')}`")
        if data.get("similar_to"):
            lines.append(f"- **Similarity:** Related to `{data.get('similar_to')}` ({int(data.get('similarity_score', 0)*100)}% intent overlap)")
        if data.get("author"):
            lines.append(f"- **Author / Credit:** {data['author']}")
        if data.get("upstream_url"):
            sha = f" (`{data['upstream_commit'][:12]}`)" if data.get("upstream_commit") else ""
            lines.append(f"- **Upstream Repo:** [{data['upstream_url']}]({data['upstream_url']}){sha}")
        lines.append(f"- **Adapter File:** [`{data.get('file')}`]({data.get('file')})")
        lines.append(f"- **Source:** {data.get('source')}")
        lines.append(f"- **Absorbed At:** {datetime.fromtimestamp(data.get('absorbed_at', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

    with open(HISTORY_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[v] Updated ABSORPTION_HISTORY.md: {HISTORY_MD_PATH}")

def extract_frontmatter(content):
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            curr_key = None
            curr_val = []
            for line in fm_text.splitlines():
                if curr_key and (line.startswith("  ") or line.startswith("\t")):
                    curr_val.append(line.strip())
                    continue
                if curr_key:
                    meta[curr_key] = " ".join(curr_val).strip().strip("'\"")
                    curr_key = None
                    curr_val = []
                if ":" in line:
                    k, v = line.split(":", 1)
                    val = v.strip()
                    if val in (">", "|", ">-", "|-"):
                        curr_key = k.strip()
                    else:
                        meta[k.strip()] = val.strip("'\"")
            if curr_key:
                meta[curr_key] = " ".join(curr_val).strip().strip("'\"")
    return meta, body

def _copy_tree_safe(src_dir, dst_dir, protected_names=None):
    """Copy directory tree recursively while preserving protected core files."""
    copied = []
    protected = protected_names or set()
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d.lower() not in IGNORED_DIRS]
        rel_root = os.path.relpath(root, src_dir)
        target_root = dst_dir if rel_root == "." else os.path.join(dst_dir, rel_root)
        os.makedirs(target_root, exist_ok=True)
        for fname in files:
            if rel_root == "." and fname in protected:
                continue
            src_file = os.path.join(root, fname)
            dst_file = os.path.join(target_root, fname)
            shutil.copy2(src_file, dst_file)
            copied.append(os.path.relpath(dst_file, OMNI_DIR).replace("\\", "/"))
    return copied

def _ingest_supporting_assets(skill_dir, scan_dir, skill_name, body):
    """Copy supporting references/scripts and adjust relative links in adapter prose."""
    assets = []
    is_root_skill = os.path.abspath(skill_dir) == os.path.abspath(scan_dir)

    src_refs = os.path.join(skill_dir, "references")
    if os.path.isdir(src_refs):
        dst_refs = REFERENCES_DIR if is_root_skill else os.path.join(REFERENCES_DIR, skill_name)
        assets.extend(_copy_tree_safe(src_refs, dst_refs))
        if not is_root_skill:
            body = re.sub(r'(\(|`)references/', rf'\1../references/{skill_name}/', body)

    src_scripts = os.path.join(skill_dir, "scripts")
    if os.path.isdir(src_scripts):
        dst_scripts = SCRIPTS_DIR if is_root_skill else os.path.join(SCRIPTS_DIR, skill_name)
        protected = PROTECTED_SCRIPTS if is_root_skill else set()
        assets.extend(_copy_tree_safe(src_scripts, dst_scripts, protected_names=protected))
        if not is_root_skill:
            body = re.sub(r'(\(|`)scripts/', rf'\1../scripts/{skill_name}/', body)

    return body, assets

def sanitize_source_path(source):
    """Replace local user home directory with '~' to keep public logs portable and private."""
    s = str(source or "")
    if not s or s.startswith(("http://", "https://")):
        return s
    home = os.path.expanduser("~")
    if home:
        norm_s = os.path.normpath(s)
        norm_home = os.path.normpath(home)
        if norm_s.lower().startswith(norm_home.lower()):
            rel = norm_s[len(norm_home):].lstrip("\\/").replace("\\", "/")
            return f"~/{rel}" if rel else "~"
    return s


def _extract_upstream_meta(source_path_or_url, scan_dir, is_git):
    """Extract normalized upstream URL, author credit, and current HEAD commit."""
    upstream_url = ""
    author = ""
    commit_sha = ""
    if is_git:
        upstream_url = re.sub(r"\.git$", "", source_path_or_url.rstrip("/"))
        if "github.com/" in upstream_url:
            author = upstream_url.split("github.com/")[-1].split("/")[0]
    git_dir = os.path.join(scan_dir, ".git")
    if os.path.isdir(git_dir):
        res = subprocess.run(["git", "-C", scan_dir, "rev-parse", "HEAD"], capture_output=True, text=True)
        if res.returncode == 0:
            commit_sha = res.stdout.strip()
    return upstream_url, author, commit_sha

def absorb_source(source_path_or_url, sync=True):
    print(f"[*] Starting OMNI Skill Absorption from: {source_path_or_url}")
    is_git = source_path_or_url.startswith("http://") or source_path_or_url.startswith("https://") or source_path_or_url.endswith(".git")
    work_dir = None
    
    if is_git:
        work_dir = tempfile.mkdtemp(prefix="omni_absorb_")
        print(f"[*] Cloning repository to {work_dir}...")
        res = subprocess.run(["git", "clone", "--depth", "1", source_path_or_url, work_dir], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[!] Clone failed: {res.stderr}")
            shutil.rmtree(work_dir, ignore_errors=True)
            return False
        scan_dir = work_dir
    else:
        scan_dir = os.path.abspath(source_path_or_url)
        if not os.path.exists(scan_dir):
            print(f"[!] Source directory not found: {scan_dir}")
            return False

    upstream_url, default_author, commit_sha = _extract_upstream_meta(source_path_or_url, scan_dir, is_git)
    reg = load_registry()
    absorbed_count = 0

    found_skills = []
    for root, dirs, files in os.walk(scan_dir):
        dirs[:] = [d for d in dirs if d.lower() not in IGNORED_DIRS]
        for file in files:
            if file.lower() == "skill.md":
                found_skills.append(os.path.join(root, file))

    if not found_skills:
        for candidate in ["AGENTS.md", "README.md"]:
            cand_path = os.path.join(scan_dir, candidate)
            if os.path.exists(cand_path):
                found_skills.append(cand_path)
                break

    print(f"[*] Found {len(found_skills)} potential skill instruction file(s).")

    sanitized_source = sanitize_source_path(source_path_or_url)
    for sf in found_skills:
        try:
            with open(sf, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()

            meta, body = extract_frontmatter(raw)
            skill_name = meta.get("name")
            if not skill_name:
                parent_name = os.path.basename(os.path.dirname(sf))
                if parent_name and parent_name.lower() not in ["skills", "adapters"]:
                    skill_name = parent_name
                else:
                    skill_name = os.path.splitext(os.path.basename(sf))[0]
            
            skill_name = skill_name.lower().replace(" ", "-")
            adapter_filename = f"{skill_name}.md"
            adapter_path = os.path.join(ADAPTERS_DIR, adapter_filename)

            body, assets = _ingest_supporting_assets(os.path.dirname(sf), scan_dir, skill_name, body)

            # Evaluate novelty against existing adapters
            relation, similar_to, sim_score, categories = evaluate_novelty(skill_name, body, reg)
            
            adapter_content = f"""# OMNI Capability Adapter: {skill_name}
> Ingested from: {sanitized_source}
> Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> Classification: {relation} (Similarity: {int(sim_score*100)}% with {similar_to or 'None'})
> Categories: {', '.join(categories)}

{body}
"""
            with open(adapter_path, "w", encoding="utf-8") as f:
                f.write(adapter_content.strip() + "\n")

            now_ts = int(datetime.now().timestamp())
            tokens = list(extract_tokens(skill_name + " " + body[:2000]))
            entry = {
                "source": sanitized_source,
                "upstream_url": upstream_url or reg.get("adapters", {}).get(skill_name, {}).get("upstream_url", ""),
                "author": meta.get("author") or default_author or reg.get("adapters", {}).get(skill_name, {}).get("author", ""),
                "upstream_commit": commit_sha or reg.get("adapters", {}).get(skill_name, {}).get("upstream_commit", ""),
                "last_checked": now_ts,
                "file": f"adapters/{adapter_filename}",
                "description": meta.get("description", f"Capability adapter for {skill_name}"),
                "absorbed_at": now_ts,
                "triggers": meta.get("argument-hint", ""),
                "relation": relation,
                "similar_to": similar_to,
                "similarity_score": sim_score,
                "categories": categories,
                "tokens": tokens[:50]
            }
            if assets:
                entry["assets"] = assets
            reg["adapters"][skill_name] = entry
            absorbed_count += 1
            extra = f" | Assets: {len(assets)}" if assets else ""
            print(f"  [+] Absorbed: {skill_name} | Relation: {relation} | Similar to: {similar_to} ({int(sim_score*100)}%){extra}")
        except Exception as e:
            print(f"  [-] Error reading {sf}: {e}")

    save_registry(reg)
    generate_markdown_history(reg)

    if work_dir and os.path.exists(work_dir):
        shutil.rmtree(work_dir, ignore_errors=True)

    print(f"\n[v] Done. Processed {absorbed_count} adapter(s).")
    if sync:
        sync_to_cluster()
    return True

def load_cluster_nodes():
    """Load user-configured cluster nodes from env override, local nodes.json, or global config."""
    candidates = [
        os.environ.get("OMNI_NODES_CONFIG", "").strip(),
        os.path.join(OMNI_DIR, "nodes.json"),
        GLOBAL_NODES_CONFIG,
    ]
    cfg_path = next((p for p in candidates if p and os.path.isfile(p)), None)
    if not cfg_path:
        return []

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print(f"[!] Failed to read cluster config {cfg_path}: {e}")
        return []

    raw_nodes = raw.get("nodes", []) if isinstance(raw, dict) else (raw if isinstance(raw, list) else [])
    nodes = []
    for item in raw_nodes:
        if isinstance(item, str) and item.strip():
            host = item.strip()
            nodes.append({"name": host, "host": host, "remote_dir": "~/.gemini/config/skills/omni", "shell": "posix"})
        elif isinstance(item, dict) and item.get("enabled", True) and item.get("host"):
            host = str(item["host"]).strip()
            rdir = str(item.get("remote_dir") or "~/.gemini/config/skills/omni").strip().rstrip("\\/")
            shell = str(item.get("shell") or ("powershell" if re.match(r"^[A-Za-z]:", rdir) else "posix")).lower()
            nodes.append({
                "name": str(item.get("name") or host).strip(),
                "host": host,
                "remote_dir": rdir,
                "shell": shell,
            })
    return nodes


def _posix_remote_expr(remote_dir):
    return f'"$HOME/{remote_dir[2:]}"' if remote_dir.startswith("~/") else f'"{remote_dir}"'


def sync_to_cluster(nodes=None, runner=None):
    """Package OMNI assets and replicate them across user-configured SSH cluster nodes."""
    target_nodes = load_cluster_nodes() if nodes is None else nodes
    if not target_nodes:
        print("\n[*] No cluster nodes configured. Set ~/.gemini/config/omni-nodes.json or nodes.json to enable sync.")
        return {"synced": [], "failed": []}

    run_cmd = runner or subprocess.run
    print(f"\n[*] Synchronizing OMNI to {len(target_nodes)} configured cluster node(s)...")
    bundle_fd, bundle_path = tempfile.mkstemp(prefix="omni_sync_", suffix=".tar.gz")
    os.close(bundle_fd)
    synced, failed = [], []
    try:
        with tarfile.open(bundle_path, "w:gz") as tar:
            for item in ["SKILL.md", "README.md", "registry.json", "ABSORPTION_HISTORY.md", "adapters", "references", "scripts"]:
                full_item = os.path.join(OMNI_DIR, item)
                if os.path.exists(full_item):
                    tar.add(full_item, arcname=item)

        for node in target_nodes:
            name = node.get("name") or node["host"]
            host = node["host"]
            remote_dir = node["remote_dir"]
            remote_tar = f"{remote_dir}/omni_sync.tar.gz"
            shell = node.get("shell", "posix")
            try:
                if shell == "powershell":
                    mk_cmd = f"powershell -Command \"New-Item -ItemType Directory -Path '{remote_dir}' -Force | Out-Null\""
                    ex_cmd = f"powershell -Command \"tar -xzf '{remote_tar}' -C '{remote_dir}'; Remove-Item '{remote_tar}' -Force\""
                else:
                    r_expr = _posix_remote_expr(remote_dir)
                    t_expr = f"{r_expr}/omni_sync.tar.gz" if r_expr.startswith('"$HOME') else f'"{remote_tar}"'
                    mk_cmd = f"mkdir -p {r_expr}"
                    ex_cmd = f"tar -xzf {t_expr} -C {r_expr} && rm -f {t_expr}"

                run_cmd(["ssh", host, mk_cmd], check=True)
                run_cmd(["scp", bundle_path, f"{host}:{remote_tar}"], check=True)
                run_cmd(["ssh", host, ex_cmd], check=True)
                synced.append(name)
                print(f"  [v] Node {name} synchronized.")
            except Exception as e:
                failed.append(name)
                print(f"  [!] Failed to sync {name}: {e}")
    finally:
        if os.path.exists(bundle_path):
            os.remove(bundle_path)
    return {"synced": synced, "failed": failed}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--no-sync"]
    do_sync = "--no-sync" not in sys.argv[1:]
    if not args:
        print("Usage: python absorb.py <github_url_or_local_path> [--no-sync]")
        sys.exit(1)
    absorb_source(args[0], sync=do_sync)
