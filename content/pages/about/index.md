---
title: How the site is run, and the rules it is built to
description: The team of agents the site is designed for, the board of work, the house rules every sgit repository follows, and the honest column of what is not yet met.
status: first
---
# How the site is run

investor.sgit.ai is designed to be run like the [PHP newsroom](https://php.oct.2026.newsroom.sgit.ai/): by a small team of agents on a schedule, with people deciding and signing. It is smaller than that newsroom's team of two people and nineteen agents and roles, but it keeps the same workflow.

## The team {#the-team}

Each role is a file in the repository's `team/roles/` folder, with what it may do and what it may not. Each runs under an [Agent Behaviour Policy](https://riskmandate.ai/abp.html), kept in `team/policies/`.

{{ team.roles }}

Messages and requests go into an append lane, `team/inbox/`: one file per message, never edited after it is written.

## The board {#the-board}

The work, as files in `team/board/`, each with a status line. This list is read from those files on every build.

{{ team.board }}

## The house rules

The repository follows sgit.ai's [guidance for every repository](https://sgit.ai/docs/guidance/repositories.md) from its first commit:

- **The brief, published in full.** [The brief](/about/brief.html), as written, never edited afterwards.
- **A reality file** that says what exists. A feature that is not in the reality file does not exist.
- **A corrections file** that says where the brief was wrong, and what was done instead.
- **CI owns the version.** The pipeline picks every number, the last one on `dev` and the middle one on `main`; no agent works out the next number itself. [CI owns the version](https://newsroom.sgit.ai/articles/ci-owns-the-version.html) explains why.
- **A gate that fails the build:** links that resolve, no orphan pages, a `.md` twin and an `llms.txt` entry for every page, scripts that parse, nothing loaded from outside the site, no em-dashes in prose, and a leak tripwire.
- **Tests against real things:** the real build, the real arithmetic in both languages, and a negative control for each check.
- **Read keys may be published; vault keys never.**

The house standards live on their own sites: [coding.sgit.ai](https://coding.sgit.ai/) for the code, [nfrs.sgit.ai](https://nfrs.sgit.ai/) for the non-functional requirements, and [ux.sgit.ai](https://ux.sgit.ai/), which measures the user experience across the sgit.ai sites.

## The honest column {#honest-column}

What the rules ask for and this first version does not yet do, said plainly. The row for nfrs.sgit.ai is kept in the repository at `admin/nfrs-row.md`.

| Asked for | State |
|---|---|
| Release verified live after deploy | Written into the pipeline; not yet run, because the site has no tagged release yet |
| `review/` folder | Intent written from the brief; the code graph and the navigator are not built |
| Type_Safe Python | Not used: the build is stdlib Python with plain classes, so it fetches nothing; recorded in the corrections file |
| Actions pinned by commit hash | Pinned by major version for now; recorded in the corrections file |
| Agent sessions' keys published with their role | Not yet: no agent has run on a schedule here |
| Custom domain | The repository is ready for it; the DNS and Pages settings are a person's step |

## What this does not claim

- **The team is designed, not running.** This first version was built in one session by one agent from the brief.
