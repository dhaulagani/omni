# OMNI Capability Adapter: project-structure
> Origin: core_skills (~\.gemini\config\skills\project-structure\SKILL.md)
> Ingested: 2026-11-10 09:34:14
> Classification: DISTINCT_CAPABILITY (Related: craft-anything, Sim: 4%)
> Categories: Testing & Quality Assurance, Debugging & Root Cause, Frontend & Human Design, Memory & Knowledge Continuity, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning, Web Intelligence & Media

# Clean Project Structure & Directory Standardization Skill

This skill enforces strict directory segregation, preventing repository root clutter and ensuring maintainability across all software and AI projects.

---

## 1. When to Apply
- Initializing a greenfield project or repo.
- Scaffolding a new microservice, tool, or pipeline.
- Auditing and un-cluttering an existing repository where scripts, tests, data, and notes are mixed in the root.

---

## 2. Directory Architecture Selection Guide

| Project Type | Target Layout Archetype | Core Subdirectories |
| :--- | :--- | :--- |
| **Python Libraries & CLI** | PEP 518/621 `src/` layout | `src/<pkg>/`, `tests/`, `scripts/`, `docs/`, `config/` |
| **Web Frontend / Fullstack** | Feature-First Colocation | `src/components/`, `src/features/`, `public/`, `tests/`, `scripts/` |
| **Data Science / ML** | Cookiecutter Data Science / Hydra | `src/`, `notebooks/`, `data/raw/`, `data/processed/`, `artifacts/`, `configs/` |
| **Go Backend** | Standard Go Project Layout | `cmd/<app>/`, `internal/`, `pkg/`, `api/`, `scripts/`, `docs/` |
| **Automation / Tooling** | Modular Script Suite | `scripts/`, `tests/`, `config/`, `docs/`, `logs/` |

---

## 3. Scaffolding Templates

### A. Python / Data Science Scaffolder
```bash
# Run from repository root
mkdir -p src/${PROJECT_NAME:-app} tests/{unit,integration} scripts config docs data/{raw,processed} logs temp
touch src/${PROJECT_NAME:-app}/__init__.py
touch tests/__init__.py tests/conftest.py
touch .env.example
```

PowerShell equivalent:
```powershell
$dirs = @(
    "src\app", "tests\unit", "tests\integration", "scripts",
    "config", "docs", "data\raw", "data\processed", "logs", "temp"
)
foreach ($d in $dirs) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
New-Item -ItemType File -Path "src\app\__init__.py", "tests\__init__.py", "tests\conftest.py", ".env.example" -Force | Out-Null
```

### B. Standard `.gitignore` Generator
Always scaffold a protective `.gitignore` to prevent data, logs, and artifacts from leaking into git:
```text
# Environment & Secrets
.env
*.local

# Python
__pycache__/
*.py[cod]
.venv/
venv/
*.egg-info/
dist/
build/

# Node / Web
node_modules/
.next/
out/

# Data & Runtime Dumps
data/
logs/
temp/
scratch/
*.log
*.sqlite3
```

---

## 4. Triage & Un-cluttering Protocol for Existing Projects

When encountering a messy directory with mixed-up files in root:

1. **Inventory Root Files**:
   List all non-standard files in root (files that are not README, LICENSE, manifests, or top-level configs).
2. **Classify & Relocate**:
   - Move test scripts (`test_*.py`, `check_*.py`, `*_test.go`) → `tests/`
   - Move standalone runner scripts (`run_*.ps1`, `setup_*.bat`, `train.py`) → `scripts/`
   - Move tabular/CSV/JSON datasets (`*.csv`, `*.xlsx`, `export.json`) → `data/raw/` or `data/processed/`
   - Move architecture notes, markdown guides, and specifications → `docs/`
   - Move generated charts, screenshots, and diagrams → `artifacts/` or `docs/assets/`
3. **Fix Imports & Path References**:
   Update relative import statements (`sys.path.append`, relative module imports, or environment working dirs) to reflect relocated paths.
4. **Smoke-Test Execution**:
   Run tests from the repository root to verify no broken paths or missing module errors.
