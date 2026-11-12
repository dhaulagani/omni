# OMNI Capability Adapter: mue-x
> Origin: core_skills (~\.gemini\config\skills\mue-x\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: DISTINCT_CAPABILITY (Related: code-review, Sim: 3%)
> Categories: Code Minimization & Pragmatism, Testing & Quality Assurance, Debugging & Root Cause, Memory & Knowledge Continuity, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning, Web Intelligence & Media

# MUE-X AST Self-Evolution & Pattern Absorption Skill

This mandatory skill defines the autonomous code self-evolution and pattern crystallization engine. Whenever refactoring complex code, modifying agent logic, or hardening modules against recurring failures, agents must apply the MUE-X AST mutation architecture.

---

## 1. Core Principles
1. **AST Over Regex**: Never perform bulk structural modifications or code rewriting using brittle regex or blind string replacement. Always parse the target file into a Concrete/Abstract Syntax Tree (`ast.parse` in Python, Tree-sitter / Babel / TS Compiler API in JS/TS).
2. **Deterministic Hardening**: Every mutation must be validated against a pre-flight syntax check (`ast.parse()`, `tsc --noEmit`, or linter) before being applied to the file system.
3. **Anti-Cancer Safeguards**:
   - Gene / file limit: Keep modular genes strictly under **800 lines**.
   - Mitosis: If a gene exceeds 800 lines, trigger automatic mitosis (split into focused sub-modules).
   - Pruning: Remove dead code, unreachable branches, and redundant helper functions.
4. **SHA-256 Deduplication**: Compute file and AST hashes to ensure no identical duplicate functions or redundant modules are created.

---

## 2. Six AST Mutation Strategies
When evolving or fixing a module, select one or more of these 6 AST mutation patterns:
1. **Parameter Tuning**: Adjust timeouts, retry counts, thresholds, and buffer limits inside AST node arguments.
2. **Error-Handling Injection**: Wrap volatile I/O, network requests, or JSON decoders in `ast.Try` blocks with typed exception handlers.
3. **Caching & Memoization**: Decorate expensive pure functions with deterministic cache wrappers (`@functools.lru_cache` or custom memoization).
4. **Algorithm Replacement**: Swap inefficient loops ($O(N^2)$ lookups) for hash maps or generator pipelines.
5. **Dead-Code Elimination**: Identify and remove unused imports, uncalled private helpers, and orphaned assignments.
6. **Interface Simplification**: Deepen module boundaries by hiding internal state behind simple, robust public methods.

---

## 3. GitHub & Local Pattern Absorption Loop
1. **Scan Proven Repositories**: Extract architectural patterns, robust retry algorithms, and modern idioms from curated open-source repositories.
2. **Crystallize into Skills**: Convert high-value absorbed patterns (*atouts*) into modular, reusable skills in `.agent/skills/` or `~/.gemini/config/skills/`.
3. **Provenance & Attribution**: Preserve license headers and original source links when absorbing external logic.

---

## 4. Execution Protocol
Whenever MUE-X self-evolution is actively triggered:
1. Read existing AST and current fitness metrics.
2. Formulate the mutation diff in an isolated AST node transformer.
3. Verify compilation:
   ```python
   import ast
   ast.parse(modified_source)
   ```
4. Write modified source to disk and execute unit tests or smoke tests.
5. Record evolution progress and absorbed patterns in the workspace log.
