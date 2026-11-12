# OMNI Capability Adapter: defuddle
> Ingested from: https://github.com/kepano/obsidian-skills
> Timestamp: 2026-11-12 09:09:06
> Classification: EXACT_REVISION (Similarity: 100% with defuddle)
> Categories: Debugging & Root Cause

# Defuddle

Use Defuddle CLI when the user wants clean Markdown extracted from a web page. It removes navigation, ads, and other page clutter.

Check availability with `defuddle --help`. If it is missing, explain the dependency and offer installation with `npm install -g defuddle`. Do not claim extraction succeeded if the tool is unavailable or returns an error.

## Usage

Always use `--md` for markdown output:

```bash
defuddle parse <url> --md
```

Save to file:

```bash
defuddle parse <url> --md -o content.md
```

Extract specific metadata:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |
