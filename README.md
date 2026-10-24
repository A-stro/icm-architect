# icm-architect

A Claude skill that designs any process, idea, or problem into an **ICM workspace** (folder structure as agent architecture), or restructures an existing folder, repo, or vault into one.

ICM (Interpretable Context Methodology) replaces orchestration code with structure: numbered folders carry sequencing, hierarchy carries context scoping, plain markdown files carry state. One agent, reading the right files at the right moment, does the work of a multi-agent framework, and a person can open any folder and see what state the system is in.

- Paper: [Interpretable Context Methodology: Folder Structure as Agent Architecture](https://arxiv.org/abs/2603.16021) (Van Clief & McDermott)
- Community: [Clief Notes](https://www.skool.com/cliefnotes)

## What it does

Two modes:

- **Build**: extracts the structure already present in how you describe your work (the stages, the checks, what's stable vs. per-run), picks a form, and scaffolds the smallest workspace that carries it.
- **Restructure**: audits an existing folder, classifies every file (catalog / contract / factory / product / dead), finds what points at each one, proposes a migration map for approval, then migrates and validates.

Every ICM is built from three primitives: a **sequence** (numbered steps, each one's output the next one's input), a **shelf** (a folder of same-shaped files), and a **catalog** (a small file that points down). The forms are recipes over them: **Pipeline**, **Record library**, **Knowledge bundle** (including one built from transcripts and research, with every quote checked against its source), **Context map**, and **System map**. They nest.

Every step ends at a **check** (a person, a script, or a small model) so a wrong turn is caught before the next step amplifies it. Every result is validated with the **walk test**: an agent with no memory must orient, act, and report status from the files alone.

The `assets/tools/` scripts (standard-library Python) check that links and input paths resolve, draw a workspace or several of them as one interactive graph, generate indexes, and check quotes against their sources.

## Install

**Claude Code:** copy this folder to `~/.claude/skills/icm-architect/` (or `.claude/skills/icm-architect/` inside a project), then ask Claude to "ICM this" / "structure this for agents" / "build me a workspace for X".

**Claude apps:** upload `icm-architect.skill` (build it with the skill-creator packager, or zip the `icm-architect/` folder itself: the folder is the zip root, not its contents) via [Customize → Skills](https://claude.ai/customize/skills).

MIT licensed, like the protocol it serves.
