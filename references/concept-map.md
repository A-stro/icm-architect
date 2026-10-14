# Concept map — ideas and their evidence, shaped to build from

The seventh form. Read this when the repeating unit is **an idea someone will teach or write up**. Sources go in (transcripts, interviews, notes, papers, the reasoning behind a codebase). Artifacts come out later (a lecture, a course, a script, an article, a doc set). The deliverable is not the artifact. It is the graph between the two: what the ideas are, whose words and evidence back each one, where each one stops, and which artifact uses which.

Two roles, named once. The **speaker** is whoever's words are in the sources (an interviewee, a lecturer, a writer). The **author** is whoever will build the artifact and answer for it. Often they are the same person. When they are not, “in their words” means the speaker's, and every list of open questions splits in two: what only the speaker can supply, and what only the author can decide.

Do not restate the ten invariants or the other six forms. Those live in `SKILL.md` and `forms.md`.

## When to use it

The user wants to work out what they know before they write from it: “plan the knowledge first,” “get my own words back out of these transcripts,” “what do I actually teach,” “map the ideas for a course,” “structure this before I script it.” Usually the sources are long, the artifacts are several, and the wording has to stay the speaker's.

Do **not** use this form when the unit is:

- a repeating production line (Pipeline)
- an organization (Context map)
- a model of how a person or subject thinks (Knowledge bundle). The two compose: the bundle carries the voice, the concept map carries the ideas of one lecture.
- a tree someone will edit (System map). Documenting code stays System map: nouns, movements, what a change hits. Add a concept map only for the ideas a newcomer must hold before those cards make sense.

Size it to the corpus. Scale the notes to the ideas, not to the length.

| Corpus | Build |
|---|---|
| one short source, one artifact | an outline; stop |
| a short corpus feeding several artifacts, or whose wording must stay the speaker's | a **light map**: `sources/`, `concepts/`, the plans. Add `checks/` only when a claim leans on an outside fact. One root `CONTEXT.md` can hold the shelf contracts. Generate `_index.md` once there are about ten notes |
| long sources (tens of thousands of words), or several artifacts sharing ideas | the full tree below |

## What the map is

The sources stay the source of truth. Every other shelf cites them and never replaces them.

| Shelf | Holds | Answers |
|---|---|---|
| `sources/` | verbatim copies of the raw material, one note per source | where did this come from, how do I cite it, what is wrong or missing in it |
| `concepts/` | one idea per file, with the speaker's words and their limits | what is this, and what did they say about it |
| `plans/` | one artifact per file: its route through the concepts | what do I need to build this |
| `checks/` | claims to verify, lines to rework, what stays out | what must be fixed before this is said |

Add `asks/` (questions to put to someone), `stories/` (worked cases) or `reading/` (where to send people) only when someone would query them. The type set is closed once, in `_meta/schema.md`.

## Target tree (smallest that carries the work)

```
<subject>-map/
├─ CLAUDE.md                 L0 catalog (twin: AGENTS.md, a one-line pointer)
├─ _meta/
│  ├─ schema.md              closed note types, citation format, privacy rules
│  ├─ sources.txt            optional: short citation key = raw file name
│  └─ keep-out.txt           phrases that must never appear anywhere in the map
├─ _templates/               concept.md, plan.md, source.md, check.md, shelf-CONTEXT.md
├─ _tools/check-concept-map.py
├─ sources/                  CONTEXT.md, _index.md, raw/ (verbatim, never edited), one note per source
├─ concepts/                 CONTEXT.md, _index.md, one idea per file
├─ plans/                    CONTEXT.md, _index.md, one artifact per file, plus map.md
└─ checks/                   CONTEXT.md, claims-to-check.md, lines-to-rework.md (only if there is something to put in it)
```

Do not create shelves for types you will not use. Each shelf's `CONTEXT.md` is its contract: what it holds, what a note in it must carry, what a person checks. Its `_index.md` is generated: `python -I _tools/check-concept-map.py --write-indexes` writes one line per note from its title and description, and the checker flags a stale one. Never hand-edit it. There is no root `CONTEXT.md` and no questionnaire in this form: `_meta/schema.md` is the schema, and slice 0 is the questionnaire.

Where it lives: a folder of its own next to the work it serves, or a shelf inside an Umbrella. If a Pipeline builds the artifacts, its first stage lists one plan and the concepts that plan names as Inputs, never the whole map.

## Citations

A quoted line ends with `(key position)`, for example `"…" (interview 12:30)`. The key is the raw file's name without its extension, or a short name declared in `_meta/sources.txt` (`iv = interview-2026-03-02.md`). Paraphrase takes no quote marks and no citation.

- **Transcripts:** the position is a timestamp (`12:30`, `1:02:15`) or a range (`12:30-13:05`). Cite the timestamp that opens the paragraph the line is in. The checker accepts a quote within one paragraph of its cited position, because a line can straddle two; a citation further off fails.
- **Documents:** the position is a page (`handout page 2`, `handout pp 4-5`). A document with lines that read `Page 1`, `Page 2` is checked by page. Any other document is matched anywhere, and its position is not checked.
- **Names:** to keep a name out of a quoted line, cut it: `"A regular ... told me she would have paid more" (interview 02:25)`. Never swap a word inside quote marks.

## Notes in this form

**Concept** (copy `_templates/concept.md`). Required sections:

1. The idea, stated once, in two or three sentences. It says only what the quoted lines say.
2. **In their words**: verbatim lines, each with a citation. Trim to the clean part; never tidy the wording.
3. **Where it stops**: the speaker's own limits and hedges. The loud version of an idea is rarely all of it.
4. **Note**: your reading, marked as a proposal. Anything beyond the quoted lines belongs here. Delete the section if you have none.
5. **Related**: links to other concepts and to the plans that use it.

**Source** (copy `_templates/source.md`). How to cite it, the words the transcription gets wrong with their fixes, where it stops short or holds only one voice (**Gaps**), and what stays out. Say what and where; the phrases themselves go in `_meta/keep-out.txt`.

**Check** (copy `_templates/check.md`). One block per claim: the speaker's quote with its citation, what it leans on, how and when it was checked, a status, and the safe line. The speaker's words never share a line with your verdict.

**Plan** (copy `_templates/plan.md`). Who it is for and what they arrive with, the one idea, what they leave able to do, a draft opening line that orients before it hooks, the spine (concepts in order, each with why it is there and whether it gets the full treatment or a line), the speaker's best lines copied from the concepts, the real thing to show, the checks that apply, and **Open**, split between the speaker and the author. A plan holds a route, not the artifact; if the script is in the plan, move it out. Give an artifact its own plan when it needs its own spine, best lines and Open list: a three-part email course is three plans. If the set is one artifact, `plans/map.md` is that plan. Otherwise it covers the set: the few ideas everything rests on, the artifacts in a suggested order with status, and the decisions only the author can make.

One home per fact, so a gap is written once. A verifiable fact lives in `checks/`. A gap in a source lives in that source's note. A question only the speaker can answer lives in the plan's Open list, and “Real thing to show” points to it. Concepts link to these; they do not repeat them.

## Build pipeline (human-gated slices)

Stop after each slice. A person reads the output before the next slice starts. This pipeline replaces Build mode steps 1 and 3 to 5.

### 0 — Frame

Ask what will be built and for whom. Ask who the speaker is, who the author is, and who answers each gate. Ask whose words must survive, what must not be said (names, embargoes, client confidences), and what a citation points at (a time, a page). List the sources and the artifacts. Propose the note types and get approval.

### 1 — Set up and bring the sources in

Copy each source into `sources/raw/` untouched. Write one source note each, leaving its Parts table for slice 2. From this skill's `assets/`, copy `templates/concept-schema.md` to `_meta/schema.md`, `templates/keep-out.txt` to `_meta/keep-out.txt` (names and anything the speaker asked to keep out go in now; matching is whole-word, so list each form: `budget`, `budgets`), `templates/concept-CLAUDE.md` to `CLAUDE.md` (with `AGENTS.md` as a one-line pointer to it), the cards you need to `_templates/`, and `tools/check-concept-map.py` to `_tools/`. The checker should pass before any concept exists.

### 2 — Read all of it

Read every source whole before writing a note. Sampling gives a map of the opening. List the distinct ideas each source makes, once each, and cluster them by how the artifact will ask for them, not by where they appeared. Write a stub for every planned note, concepts, plans and checks alike (frontmatter with `status: stub`, a title, a one-line description), so links resolve from the first batch. Fill each source note's Parts table. Present the cluster list. The speaker or author adds, merges, drops.

### 3 — Concepts

Fill the stubs one batch at a time, and write each shelf's `CONTEXT.md` (from `_templates/shelf-CONTEXT.md`) when you first fill that shelf. Run the checker after every batch and fix the note, never the raw source. Read the warnings, and read the cuts with `--show-cuts`: a cut can change a meaning, and the checker fails one that drops a negation. A reviewer reads three notes: does it sound like the speaker, does it say what they meant?

### 4 — Checks

For every outside fact a concept leans on: if you can search, verify it, write the safe version of the line, and record how and when it was checked. A search summary is a lead, not a source; say so. If you cannot search, write the claim, what would settle it and where to look as a to-look-up list for the human. Either way a claim that is not verified is marked “not checked,” dated, and kept out of the plan's best lines. List the lines to rework (tone, transcription errors) and what stays out. Do this before any plan.

### 5 — Plans

One per artifact, then `plans/map.md` if there are several. If the sources are the speaker's and not the audience's, write the audience's question in “Arrives with” as an assumption and list the audience's own words under Open. The author reads the plans before any artifact is written. The map stops here; building the artifact is a Pipeline's job.

### 6 — Walk it

Run the walk test below. No stub should be left.

## What the checker enforces

`assets/tools/check-concept-map.py`, standard library only. Run it after every batch.

- **Fails on:** a broken link; a note with no type or a type outside the schema; a quote not found near its cited position or on its cited page; a citation with no timestamp or page; an unknown source key; a bullet under “In their words” with no cited quote; a cut that drops a negation or leaves a piece too short to verify; a keep-out phrase anywhere outside `sources/raw/` and `_meta/` (frontmatter, indexes and entry files included; case-insensitive, whole words); a stale `_index.md`.
- **Warns on:** a quote found in a neighboring paragraph, not the cited one; quoted words of eight or more with no citation; stub notes that remain.
- **Options:** `--show-cuts`, `--write-indexes`, `--tokens PLAN` (the walk test's size check).

A script can prove a quote is in the source. It cannot prove a paraphrase is fair, or that a synonym of a kept-out phrase is absent; that is what the reviewer's three notes are for.

## Defining moves

- **Quotes are word for word, cited, and checked by script.** A quote the checker cannot find is a typo or an invention; either way it does not ship.
- **The speaker's words and yours never share a line.** Verbatim sits under “In their words”. Your reading sits under “Note” and is a proposal.
- **One idea, one note.** Plans and other notes link; they do not copy.
- **Gaps are named, not filled.** Open lists name what only someone can supply: a story the speaker has not told, a number they have not given. Do not write it for them. Where the sources disagree with each other, say so in the concept's “Where it stops” and ask; do not reconcile them.
- **People in the sources are described by role, never named,** in every note, with neutral pronouns unless the source states them. Names live only in the raw copies. Later agents read the notes, never the raw copies, so a name cannot travel.
- **Facts are checked before the plan, not after the artifact.**

## Walk test (this form)

A cold agent, no memory of the sources:

1. Open `CLAUDE.md`. Can it say what artifacts exist and where to start?
2. Open one plan. Can it list the spine and the speaker's best lines without opening a raw source?
3. Run the checker. Does it pass, with no stub left?
4. Open one concept. Does the unmarked paragraph say only what the quoted lines say? Anything beyond them sits under Note.
5. Does any plan answer an Open item itself?
6. Size check: `--tokens` on one plan stays under 8,000. The 2,000 floor is a guide for a full-size step, not a target for a small map.

If a step fails, split or move files. Do not add a “how to read this map” note.

## Failure modes

- Summarizing the source instead of splitting it into ideas. The graph becomes a second transcript.
- Quotes tidied “for readability.” They stop matching, or there is no check at all.
- The same idea restated per artifact. One home.
- A plan that contains the script.
- Mapping only the loud version of an idea: no “Where it stops.”
- Smoothing over a disagreement between sources instead of asking.
- Filling a spine with stories the source does not contain.
- Names, client details, or embargoed lines in notes.
- Checks written after the artifact.
- Trusting the checker for what it cannot see: whether a paraphrase is fair.
- Note types multiplying past what anyone queries.
- A hand-edited `_index.md`.
