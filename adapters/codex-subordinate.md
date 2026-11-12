# OMNI Capability Adapter: codex-subordinate
> Origin: plugin:codex-subordinate (~\.gemini\config\plugins\codex-subordinate\skills\codex-subordinate\SKILL.md)
> Ingested: 2026-11-10 09:34:14
> Classification: DISTINCT_CAPABILITY (Related: implement, Sim: 6%)
> Categories: Code Minimization & Pragmatism, Testing & Quality Assurance, Frontend & Human Design, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning

# Codex Subordinate Orchestration Skill

This skill guides the primary agent in delegating bounded programming tasks to **OpenAI Codex** (via the Codex CLI or the Codex desktop application) as a subordinate worker.

## Overview

When orchestrating Codex as a subordinate:
- **Primary Agent (Supervisor)**: High-level architectural planning, task decomposition, user interaction, security boundaries, and final diff review.
- **Codex Subordinate (Worker)**: Code generation, repetitive refactoring, unit test suite writing, and isolated patch generation.

```
+-------------------------------------------------------------+
|                 Primary Supervisor (Antigravity)            |
+-------------------------------------------------------------+
         |                                           ^
   1. Delegate Bounded Task                     5. Report & Diff
   (with test criteria)                               |
         v                                            |
+-------------------------------------------------------------+
|                 Codex Subordinate Worker                    |
|  - Subagent: codex-subordinate                              |
|  - CLI Dispatcher: codex_dispatcher.py / dispatch.ps1       |
|  - External Engine: `codex exec` or Codex Desktop App       |
+-------------------------------------------------------------+
         |                                            ^
   2. Execute Changes                            4. Verify Tests
         v                                            |
+-------------------------------------------------------------+
|                Workspace / Worktree / Files                 |
+-------------------------------------------------------------+
```

---

## 1. Interaction Modes

### Mode A: Headless CLI Execution (`codex exec`)
Best for automated, non-interactive tasks where Codex directly edits files in the current repository:
```bash
# Cross-platform via python dispatcher:
python "~/.gemini/config/plugins/codex-subordinate/skills/codex-subordinate/scripts/codex_dispatcher.py" \
  --task "Implement unit tests for src/auth/jwt.py covering expired tokens and malformed signatures" \
  --verify-cmd "pytest tests/test_jwt.py" \
  --dangerously-skip-permissions
```

On Windows with PowerShell:
```powershell
& "~\.gemini\config\plugins\codex-subordinate\skills\codex-subordinate\scripts\dispatch.ps1" `
  -Task "Refactor UserService to use dependency injection" `
  -VerifyCmd "npm test" `
  -SkipPermissions
```

### Mode B: Isolated Git Worktree (Codex Desktop App & CLI)
When working with the Codex Desktop Application or executing large structural changes, isolate the subordinate in a Git worktree:

1. **Create an isolated worktree**:
   ```bash
   git worktree add ../repo-codex-worker -b feature/codex-subordinate-task
   ```
2. **Assign the worktree to Codex**:
   - In Codex CLI: Run `codex` inside `../repo-codex-worker`.
   - In Codex Desktop Application: Open the folder `../repo-codex-worker` as a supervised project thread.
3. **Supervisor Review**:
   Once Codex finishes the work:
   ```bash
   git -C ../repo-codex-worker status
   git -C ../repo-codex-worker diff
   ```
4. **Merge or Clean Up**:
   If verified, merge the branch into main and remove the worktree:
   ```bash
   git worktree remove ../repo-codex-worker
   ```

### Mode C: Subagent Invocation (`codex-subordinate`)
Invoke the bundled Antigravity subagent directly when running inside an Antigravity conversation:
```json
{
  "TypeName": "codex-subordinate",
  "Role": "Codex Subordinate Worker",
  "Prompt": "Implement missing unit tests for the UserService class in tests/user_service_test.py. Ensure coverage for invalid email inputs. Verify using `npm test`."
}
```

---

## 2. Step-by-Step Delegation Workflow

### Step 1: Pre-flight & Baseline
1. Confirm the working tree is clean: `git status --short`.
2. Check if tests pass prior to delegation: run project test command.

### Step 2: Formulate the Subordinate Directive
A good delegation prompt must be strictly bounded:
- **Target File(s)**: Explicit relative file paths.
- **Requirements**: Specific functions to create or modify.
- **Constraints**: Do not touch unrelated files; preserve existing APIs.
- **Verification Command**: How Codex should verify its work (e.g. `pytest`, `cargo test`).

### Step 3: Dispatch Execution
Invoke `codex_dispatcher.py` or the `codex-subordinate` subagent.

### Step 4: Audit Changes
Examine the git diff:
```bash
git diff --stat
git diff
```
Ensure:
- No unauthorized dependencies or files were created.
- No secrets or sensitive data were written.
- Code conforms to project conventions.

### Step 5: Verification & Completion
Run the project's test suite and linters:
```bash
npm test || pytest || cargo test
```
If checks pass, commit the changes or hand back to the user.

---

## 3. Fallback When Codex CLI Is Unavailable

If `codex` is not installed on the system PATH:
1. The dispatcher outputs instructions on installing the Codex CLI.
2. The agent automatically falls back to the native `codex-subordinate` subagent persona to execute the requested changes directly with strict diff validation.
