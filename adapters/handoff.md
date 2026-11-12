# OMNI Capability Adapter: handoff
> Origin: core_skills (~\.gemini\config\skills\handoff\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: DISTINCT_CAPABILITY (Related: grilling, Sim: 6%)
> Categories: Code Minimization & Pragmatism, Memory & Knowledge Continuity, Reverse Engineering & Inspection, Workflow & Planning

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
