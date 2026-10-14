# Schema — the rules of this map

The closed set of note types, how quotes are cited, and what may never appear. When practice and this file disagree, reconcile the same day.

types: concept, plan, source, check

Add `ask`, `story` or `reading` to that line only when someone will query them. The checker reads the `types:` line.

## Note types

| `type:` | Lives at | Carries |
|---|---|---|
| source | `sources/<slug>.md` | how to cite, errors and fixes, gaps, what stays out |
| concept | `concepts/<slug>.md` | one idea, the speaker's words, where it stops |
| plan | `plans/<slug>.md` | one artifact's route through the concepts |
| check | `checks/<slug>.md` | claims to verify, lines to rework |

A planned note that is not written yet is a stub: its frontmatter, a title, a one-line description and `status: stub`. Links to it resolve from the first batch. The checker warns while any stub remains.

## Citations

`"verbatim line" (key position)`. The key is the raw file's name without its extension, or a short name declared in `_meta/sources.txt` as `key = filename`. Position for a transcript is `mm:ss` or `h:mm:ss` (or a range, `12:30-13:05`); cite the timestamp that opens the paragraph. Position for a document is a page (`page 2`, `pp 4-5`); a document with `Page 1`, `Page 2` lines is checked by page, and any other document is matched anywhere. Paraphrase takes no quote marks. To keep a name out of a quote, cut it with `...`; never swap a word inside the marks.

## Privacy

People are described by role, never named, in every note, with neutral pronouns unless the source states them. Phrases that must never appear go in `_meta/keep-out.txt`, one per line; the checker fails on a whole-word hit anywhere outside `sources/raw/` and `_meta/`, so list each form of a word. Keep that file out of anything that is published.

## Naming

Slugs are kebab-case. One idea per file, and the filename is the idea. Each shelf has a `CONTEXT.md` (its contract) and a generated `_index.md`.
