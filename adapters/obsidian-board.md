# OMNI Capability Adapter: obsidian-board
> Origin: core_skills (~\.gemini\config\skills\obsidian-board\SKILL.md)
> Ingested: 2026-11-10 09:34:13
> Classification: DISTINCT_CAPABILITY (Related: idea-discovery, Sim: 10%)
> Categories: Memory & Knowledge Continuity, AST & Code Intelligence, Reverse Engineering & Inspection, Workflow & Planning, Web Intelligence & Media

Use the obsidian-second-brain skill. Execute `/obsidian-board $ARGUMENTS`:

The optional argument is a board name. Handle typos and partial matches.

1. Read `_CLAUDE.md` first if it exists in the vault root
2. If a board name is given, search `Boards/` for it (fuzzy match)
3. If no name given, list available boards and ask which one
4. Read and display the current board state: columns, item counts, overdue items (past `@{date}`)
5. Ask if the user wants to make updates - if yes, infer changes from conversation context
6. Move completed items to ✅ Done with strikethrough, add new items in the right column
7. Flag any items that are overdue or have been in the same column for more than a week

---

**AI-first rule:** Every note created or updated by this command MUST follow `references/ai-first-rules.md` - `## For future Claude` preamble, rich frontmatter (`type`, `date`, `tags`, `ai-first: true`, plus type-specific fields), recency markers per external claim, mandatory `[[wikilinks]]` for every person/project/concept referenced, sources preserved verbatim with URLs inline, and confidence levels where applicable. The vault is for future-Claude retrieval - not human reading.

**Anti-fabrication:** Search exhaustively before claiming any note, person, or file is absent - false absence is the most common failure mode - and never invent facts, entities, or dates (mark unknowns as `TBD`). See the anti-fabrication and search-completeness hard rules in `references/ai-first-rules.md`.
