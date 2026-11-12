# OMNI Capability Adapter: ctx-insight
> Origin: core_skills (~\.gemini\config\skills\ctx-insight\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: DISTINCT_CAPABILITY (Related: ctx-doctor, Sim: 8%)
> Categories: General Engineering

# Context Mode Insight

Open the hosted Insight dashboard in the user's default browser.

## Instructions

1. Call the `ctx_insight` MCP tool (no parameters). It opens
   <https://context-mode.com/insight> in the default browser and returns a
   confirmation line.
2. Display the tool's output to the user.
3. Tell the user:
   - "Insight opened at https://context-mode.com/insight"
   - The landing page at context-mode.com/insight is the single source of truth for sign-in and pricing details.
   - If the browser did not open automatically, share the URL so they can open it manually.
