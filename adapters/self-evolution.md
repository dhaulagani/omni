# OMNI Capability Adapter: self-evolution
> Origin: core_skills (~\.gemini\config\skills\self-evolution\SKILL.md)
> Ingested: 2026-11-10 09:34:14
> Classification: DISTINCT_CAPABILITY (Related: cli-hub-meta-skill, Sim: 4%)
> Categories: Code Minimization & Pragmatism, Testing & Quality Assurance, Debugging & Root Cause, Memory & Knowledge Continuity, AST & Code Intelligence, Reverse Engineering & Inspection

# Autonomous Self-Evolution & Continuous Adaptation Skill

This skill enables the agent to continuously self-improve, adapt to new environments, and expand its own capabilities without human intervention.

Inspired by state-of-the-art agent reflection architectures (such as Voyager, Reflexion, and Autonomous Skill Libraries), this skill operates across three interconnected evolutionary loops:

---

## 1. The Reflective Learning Loop (Reflexion)
Whenever a command, script, or tool execution fails or encounters unexpected behavior:
1. **Root-Cause Diagnosis**: Do not merely retry the identical failed action. Analyze the exact traceback, environment mismatch, or API constraint.
2. **Hypothesis Formulation**: Formulate a distinct alternative hypothesis (e.g., fallback endpoints, dependency incompatibility, alternate parameters).
3. **Synthesis & Memory**: Record critical lessons in the workspace memory (`.agents/rules/` or local runbooks) so the agent never repeats the same error.

---

## 2. Skill Distillation & Library Expansion (Voyager Pattern)
When solving a non-trivial, multi-step problem or discovering a working procedure:
1. **Identify Reusable Logic**: Extract parameters, helper scripts, and decision trees.
2. **Automate Modularization**: Create a new skill in `.agents/skills/<skill-name>/` with:
   - `SKILL.md`: Concise step-by-step runbook with YAML frontmatter.
   - `scripts/`: Tested, reliable automation scripts.
3. **Self-Verification**: Run a dry-run or verification test before committing the new skill.

---

## 3. Dynamic Strategy Adaptation
- **Environment Awareness**: Detect host OS, containerization (PRoot, Docker, native), and library version anomalies early.
- **Fail-Fast & Pivot**: If an external unofficial interface or API is throttled or deprecated, automatically pivot to official APIs, webhooks, or scheduled job engines without stalling.
- **Proactive Optimization**: Review code diffs and outputs against user intent and domain aesthetics before delivering final results.
