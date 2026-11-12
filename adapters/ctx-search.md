# OMNI Capability Adapter: ctx-search
> Origin: core_skills (~\.gemini\config\skills\ctx-search\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: PARTIAL_OVERLAP (Related: ctx-index, Sim: 20%)
> Categories: Code Minimization & Pragmatism, Reverse Engineering & Inspection, Workflow & Planning, Web Intelligence & Media

# Context Mode Search

Search indexed content without rereading raw sources into conversation context.

## Instructions

1. Prefer the `ctx_search` MCP tool when it is available.
2. Batch all related questions in one `queries` array.
3. Scope with `source` when the user names a project or indexed label.
4. Use short, specific queries of two to four technical terms.

```javascript
ctx_search({
  source: "project:<name>",
  queries: ["authentication middleware", "token refresh"],
  limit: 5
})
```

5. If MCP tools are unavailable, fall back to the CLI:

```bash
context-mode search "authentication middleware" --source project:<name> --limit 5
```

6. If the index is empty, tell the user to run `/context-mode:ctx-index` or `context-mode index <path>` first.
