# {Map name}

{One sentence: what this map holds and which artifacts it feeds. The artifacts themselves are not written here.}

Built on ICM, form: Concept map. The structure is the documentation; each shelf's CONTEXT.md says what belongs in it.

## What exists

| Artifact | Plan | Status |
|---|---|---|
| {artifact} | `plans/{slug}.md` | {plan · drafted · built} |

## Where things live

| Folder | What it holds |
|---|---|
| `sources/` | `raw/`: the sources, verbatim, never edited. One note per source: how to cite, gaps, what stays out |
| `concepts/` | one idea per file: the speaker's words, and where each idea stops |
| `plans/` | one artifact per file, plus `map.md` for the set |
| `checks/` | claims to verify, lines to rework, what stays out |
| `_meta/` | `schema.md`, `keep-out.txt`, optional `sources.txt` |
| `_templates/`, `_tools/` | blank starters; `check-concept-map.py` |

## Route by what you are doing

| If | Go to |
|---|---|
| building an artifact | its plan in `plans/`, then only the concepts it names |
| you need the exact words | the concept's "In their words"; the raw copy is in `sources/raw/` |
| about to say a number or a general claim | `checks/claims-to-check.md` |
| something is missing | the plan's "Open": ask, do not fill |
| adding an idea | copy `_templates/concept.md`, then run the checker |
| status | the `status:` line in each plan |

## The rules

- A quote is word for word, cited `(key position)`, and checked: `python -I _tools/check-concept-map.py`.
- The speaker's words sit under "In their words". Your reading sits under "Note", marked as a proposal. They never share a line.
- People are described by role, never named. `_meta/keep-out.txt` lists what never appears.
- Nothing moves on until a person has read the last output.
