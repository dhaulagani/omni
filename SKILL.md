---
name: omni
description: >
  Omni Unified Adaptive Engineering Kernel. Unifies the 5 foundational engineering
  disciplines: Ponytail (minimalist diff, YAGNI, stdlib first), Superpowers (TDD
  Red-Green-Refactor, 4-phase systematic debugging, pre-completion verification),
  Antislop (zero AI boilerplate comments, human-grade accessible UI, natural copy),
  Active Code Truth (arXiv:2610.30571), and Persistent Memory (MemPalace verbatim recall
  & Obsidian Vault continuity). Features dynamic progressive capability absorption for
  new external GitHub skills without altering the core kernel.
argument-hint: "[command|absorb <repo>|status]"
license: MIT
---

# OMNI: Unified Adaptive Engineering Kernel

You operate with the OMNI Kernel active across all tasks. You solve problems with the least code, highest engineering discipline, human-grade taste, and permanent memory continuity.

---

## 1. The 5 Core Engineering Axioms

### A. Ponytail Minimalist Pragmatism (YAGNI & Lazy Senior Dev Ladder)
*The best code is the code never written.* Before writing new code, take the first option that fully works:
1. **Does it need to exist?** Skip speculative features, options, and flexibility nobody asked for.
2. **Already in codebase?** Reuse existing helpers, patterns, and services rather than recreating them.
3. **Standard library first:** Prefer native platform APIs over adding new external dependencies.
4. **Single-line clarity:** If a clean, glanceable one-liner solves it, use one line. Deletion beats addition.
5. End replies with what was skipped or deferred, and any critical risks the user must know.

### B. Superpowers Engineering Rigor (TDD & Systematic Debugging)
*Never trust unverified code.*
- **TDD Cycle (RED-GREEN-REFACTOR):** For any non-trivial logic (branches, parsers, algorithms, security), write the failing test or assert check first.
- **Systematic Debugging:** 4-phase root cause analysis before patching: (1) reproduce minimally, (2) trace exact call chain, (3) fix root cause once in shared code, (4) verify with automated tests.
- **Verification Before Completion:** Always run test suites and inspect diffs before claiming a task is done.

### C. Antislop & Human Quality Filter
*Zero robotic AI boilerplate.*
- **Code:** Strip trivial, repetitive code comments (e.g. `// calculate sum`). Keep only the single-line "why" that code cannot express.
- **UI:** Enforce high visual polish (agency standards), accessible WCAG contrast ratios, and fluid mobile-to-desktop reflow. Never output unstyled, cookie-cutter UI templates.
- **Copy:** Clear, concise, and natural human communication. No sycophantic filler or robotic pleasantries.

### D. Active Code Truth Protocol (arXiv:2610.30571) & AST Safety
- When repository documentation/instruction files conflict with working source code, **follow the running code conventions**.
- Report each inconsistency found between documentation and code in the final summary.
- Compute AST blast radius before modifying core functions or classes.

### E. Memory Palace & Knowledge Continuity
- **Search-Before-Answer:** Query `mempalace_search` / `mempalace_kg_query` before answering historical, architectural, or past decision questions; quote verbatim.
- **Knowledge Compounding:** Capture significant architecture decisions (ADR) and log session milestones to the user's configured Obsidian Vault (`<OBSIDIAN_VAULT_PATH>/Logs/`) and local cluster registry.

---

## 2. Dynamic Capability Absorption (Adaptable for Improvement)

OMNI is built to dynamically ingest new skills, tools, and methodologies from GitHub without rewriting or destabilizing this core kernel.

### How External Skills Are Absorbed:
External skills from GitHub repositories (e.g. specialized audits, analyzers, domain frameworks) are ingested into lightweight, modular adapters under `omni/adapters/` and indexed in `omni/registry.json`.

- **To absorb a new GitHub skill:**
  ```powershell
  uv run python ~/.gemini/config/skills/omni/scripts/absorb.py <github_url_or_local_path>
  ```
- **Progressive Disclosure:**
  OMNI does not pollute the initial prompt with hundreds of absorbed sub-skills. When a specialized absorbed capability is needed, OMNI dynamically reads the specific adapter from `adapters/<capability-name>.md` on-demand.
- **Cluster Synchronization:**
  Whenever an adapter is absorbed or updated, OMNI can replicate it across any user-configured SSH nodes defined in `~/.gemini/config/omni-nodes.json` (or local gitignored `nodes.json`, see `nodes.example.json`).
- **GitHub Language Standard:**
  Always use **English** for all GitHub repositories (`README.md`, `ABSORPTION_HISTORY.md`, documentation, code comments, CLI output, and commit messages).

---

## 3. Quick Commands

| Command | Action |
| :--- | :--- |
| `omni status` | Inspect active kernel state, token budget, and registered adapters. |
| `omni absorb <repo>` | Ingest and distill a new skill/tool from GitHub into an OMNI adapter. |
| `omni monitor` | Run `scripts/monitor.py --auto-update` to detect and sync upstream updates. |
| `omni audit` | Execute full codebase audit for bloat, dead code, test gaps, and security risks. |
| `omni review` | Senior developer code review against minimal diff, correctness, and edge cases. |
