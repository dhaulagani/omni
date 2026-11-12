# ⚡ OMNI: The Unified Adaptive Engineering Kernel

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Works With](https://img.shields.io/badge/Works_With-Antigravity_%7C_Codex_%7C_Claude_Code_%7C_Cursor-blueviolet.svg)](#)
[![Token Efficiency](https://img.shields.io/badge/Catalog_Token_Reduction--90%25-brightgreen.svg)](#)
[![Dynamic Absorption](https://img.shields.io/badge/GitHub_Skill_Absorption-Live_Plug_%26_Play-orange.svg)](#)

> **"Unifying 150+ fragmented agent skills into a single, cohesive, self-evolving engineering engine."**  
> OMNI eliminates AI over-engineering, prompt catalog bloat, and brittle skill fragmentation by consolidating the core engineering disciplines into one native, dynamically extensible kernel.

---

## 🎯 The Problem OMNI Solves

Modern AI coding agents accumulate dozens—sometimes hundreds—of disconnected plugin instructions and skill files:
1. **Catalog Token Bloat:** Registering 140+ skill descriptions consumes over **10,000 tokens** in the opening system prompt (~52% of a typical 20,000-token customization budget).
2. **Attention Dilution & Indecision:** LLMs hesitate when choosing between overlapping skills (such as `tdd` vs `test-driven-development`, or `antislop-ui` vs `design-taste`).
3. **Rigid Fragility:** Integrating a new capability from a GitHub repository typically forces manual edits to global instruction files or brittle wrapper rewrites.

**OMNI solves this directly:** It replaces hundreds of scattered skills with **1 Unified Native Kernel** (`SKILL.md`, <100 lines) paired with an on-demand **Dynamic Capability Absorption** pipeline (`adapters/`, `references/`, and `scripts/`).

---

## 🏛️ The 5 Core Engineering Axioms

OMNI unifies five foundational engineering disciplines into a single deterministic execution loop:

```text
                      ┌────────────────────────────────────────┐
                      │      OMNI UNIFIED ADAPTIVE KERNEL      │
                      └───────────────────┬────────────────────┘
                                          │
       ┌──────────────────┬───────────────┴───────────────┬──────────────────┐
       ▼                  ▼                               ▼                  ▼
┌──────────────┐   ┌──────────────┐                ┌──────────────┐   ┌──────────────┐
│ 1. PRAGMATIC │   │ 2. ENGINEER  │                │ 3. CODE & UI │   │ 4. MEMORY &  │
│ MINIMALISM   │   │ DISCIPLINE   │                │  INTEGRITY   │   │ CONTINUITY   │
├──────────────┤   ├──────────────┤                ├──────────────┤   ├──────────────┤
│ • Ponytail   │   │ • Superpowers│                │ • Antislop   │   │ • MemPalace  │
│   (YAGNI,    │   │ • TDD Cycle  │                │   (No-slop   │   │   (Verbatim  │
│   minimal    │   │ • Systematic │                │   UI & Copy) │   │   Recall)    │
│   diff, zero │   │   Debugging  │                │ • arXiv:2610 │   │ • Obsidian   │
│   bloat)     │   │ • Pre-flight │                │   (Code over │   │   (ADR, Log, │
│ • Standard   │   │   Verify     │                │   doc truth) │   │   Vault)     │
│   Library    │   │ • Clean Arch │                │ • MUE-X/AST  │   │ • Global Node│
│   first      │   │   Structure  │                │   Safety     │   │   Cluster    │
│              │   │              │                │              │   │   Sync       │
└──────────────┘   └──────────────┘                └──────────────┘   └──────────────┘
```

1. **Ponytail Pragmatism (YAGNI & Minimal Diff):** *The best code is the code never written.* Reuse existing helpers and standard libraries before adding dependencies. Deletion beats addition.
2. **Superpowers Rigor (TDD & Systematic Debugging):** Enforce RED-GREEN-REFACTOR for non-trivial logic, 4-phase root cause investigation before patching, and automated verification before completion.
3. **Antislop & Human Taste:** Reject redundant AI comments and generic UI templates; enforce WCAG contrast, fluid mobile-to-desktop reflow, and natural copywriting.
4. **Active Code Truth (arXiv:2610.30571):** Whenever documentation and running code disagree, follow the conventions of the working codebase and report every inconsistency.
5. **Memory Palace & Vault Continuity:** Enforce *Search-Before-Answer* verbatim recall via MemPalace and log architectural decisions (ADR) and operations to the Obsidian Vault.

---

## ⚡ Dynamic Capability Absorption (Adaptable for Improvement)

OMNI can **ingest new skills, references, and supporting scripts directly from GitHub** without altering a single line of its core kernel.

### Absorbing a New GitHub Skill:
```powershell
uv run python scripts/absorb.py <github_url_or_local_path> [--no-sync]
```

### How Asset Ingestion & Progressive Disclosure Work:
* **Skill Adapters (`adapters/`):** Distills each discovered `SKILL.md` into an on-demand adapter while ignoring test fixtures (`tests/`, `fixtures/`, `node_modules/`, etc.).
* **Supporting Assets (`references/` & `scripts/`):** Copies skill-local or repository-level reference docs and helper scripts without clobbering core OMNI utilities, automatically rewriting relative paths so adapters resolve cleanly.
* **Intelligent Novelty & Similarity Detection:** Uses Jaccard token analysis to classify every absorbed skill:
  * **`EXACT_REVISION` (> 70% similarity):** Detects an updated version of an existing skill.
  * **`SIMILAR_EXTENSION` / `PARTIAL_OVERLAP` (20% - 70% similarity):** Registers domain-adjacent extensions without overwriting core adapters.
  * **`BRAND_NEW_CAPABILITY` (< 20% similarity):** Expands OMNI into new engineering or tooling domains.

Full absorption logs and metadata are maintained in [`ABSORPTION_HISTORY.md`](./ABSORPTION_HISTORY.md) and [`registry.json`](./registry.json).

---

## 📦 Absorbed Capability Ecosystem

OMNI currently unifies **156 public adapters**, including:
- **Minimalism & Code Audit:** [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) (`ponytail`, `ponytail-audit`, `ponytail-debt`, `ponytail-review`, `ponytail-gain`, `ponytail-help`).
- **Software Engineering & Testing:** Superpowers (`tdd`, `systematic-debugging`, `verification-before-completion`, `brainstorming`, `using-git-worktrees`), Antislop suite, CodeGraph, MUE-X.
- **Obsidian & Knowledge Systems:** [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) (`obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas`, `defuddle`, `knap`) and [`eugeniughelbur/obsidian-second-brain`](https://github.com/eugeniughelbur/obsidian-second-brain) (`obsidian-second-brain`, 33+ `obsidian-*` workflows, Python scanners, and reference schemas).

See the complete matrix in [`ABSORPTION_HISTORY.md`](./ABSORPTION_HISTORY.md).

---

## 🔄 Upstream Update Monitoring & Auto-Adaptation

OMNI tracks each external skill's source GitHub repository and baseline commit SHA inside [`registry.json`](./registry.json), enabling automatic upstream drift detection and self-updating without manual intervention:

```powershell
# Check all tracked upstream repositories concurrently (status only)
uv run python scripts/monitor.py

# Automatically re-absorb updated repositories and sync across cluster nodes
uv run python scripts/monitor.py --auto-update
```

A scheduled task (`OMNI-Upstream-Monitor`) can run `monitor.py --auto-update` periodically so OMNI adapts automatically whenever an upstream author ships improvements or fixes.

---

## 🙏 Credits & Upstream Attributions

OMNI stands on the shoulders of open-source engineering workflows and agent skill authors. Full skill-level attribution is tracked in [`ABSORPTION_HISTORY.md`](./ABSORPTION_HISTORY.md):

| Upstream Project | Author / Maintainer | Domain / Contribution | Absorbed Skills |
|---|---|---|---|
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | DietrichGebert | YAGNI pragmatism, minimal diffs, code audit & debt tracking | 6 |
| [obra/superpowers](https://github.com/obra/superpowers) | obra (Jesse Vincent) | TDD Red-Green-Refactor, systematic debugging, planning & verification | 15 |
| [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) | miqdadbadjuber | Zero-slop code, UI accessibility, mobile reflow & natural copy | 6 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | Senior engineering workflows (`tdd`, `triage`, `to-spec`, `grill-me`, etc.) | 27 |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | kepano (Steph Ango) | Obsidian Flavored Markdown, `.base` databases, JSON Canvas, CLI, Defuddle, Knap | 7 |
| [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | eugeniughelbur | Self-rewriting LLM Wiki & vault workflows, scanners, and AI-first schemas | 44 |
| [MemPalace/mempalace](https://github.com/MemPalace/mempalace) | MemPalace | Verbatim Search-Before-Answer memory palace & knowledge graph recall | 2 |
| [mksglu/context-mode](https://github.com/mksglu/context-mode) | mksglu | Output sandboxing, indexing, and token conservation | 9 |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | ChromeDevTools | Browser debugging, LCP optimization, memory leaks & a11y diagnostics | 8 |
| [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) | GoogleChrome | Modern Web APIs & Manifest V3 Chrome Extension best practices | 2 |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Leonxlnx | Anti-slop frontend art direction & typography taste | 1 |
| [Leonxlnx/taste-skill-classics](https://github.com/Leonxlnx/taste-skill-classics) | Leonxlnx | Minimalist, high-end visual, brutalist telemetry & Stitch design skills | 4 |
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | nexu-io | Brandkit, image-to-code, mobile/web imagegen & UI redesign workflows | 5 |
| [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | Hugo He | Routed AI slide deck & SVG presentation generation workflow | 1 |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic | Official `.pptx` XML editing, creation, and analysis skill | 1 |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | storytold | Evidence-first software inspection and clean-room reconstruction | 1 |
| [morluto/rea](https://github.com/morluto/rea) | morluto | Reverse engineering & binary/APK inspection via REA engine | 1 |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | Panniantong | Multi-platform web & social retrieval bridge | 1 |
| [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) | alexgreensh | Interactive vector animation authoring | 1 |
| [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | HKUDS | Automated CLI-wrapper generation for applications | 1 |
| Android CLI Plugin | Android Developer Tools Team | Android CLI, Compose Preview, Device Hub integrations | 3 |

---

## 🌐 Multi-Node Cluster Synchronization

Whenever a capability is absorbed or updated, `absorb.py` packages and synchronizes `SKILL.md`, `README.md`, `registry.json`, `ABSORPTION_HISTORY.md`, `adapters/`, `references/`, and `scripts/` across your own user-configured SSH nodes over SSH/SCP.

Cluster targets are **private per user** and never committed to git. Copy [`nodes.example.json`](./nodes.example.json) to your global config path or local repo config:
- Global (recommended, persists across updates): `~/.gemini/config/omni-nodes.json`
- Repo-local (gitignored): `./nodes.json`
- Custom override: `OMNI_NODES_CONFIG=/path/to/nodes.json`

```powershell
# Audit customization token budget health
node ~/.gemini/config/scripts/audit_customization_budget.js
```

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information. Copyright (c) 2026 **dhaulagani**.
