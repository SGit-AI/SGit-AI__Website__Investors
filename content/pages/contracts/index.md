---
title: Contracts as graphs: one Series A, clause by clause
description: Startup contracts, cap tables and term sheets as linked documents with their versions and caveats. One fictional Series A, every clause a node.
status: first
order: 2
short: Contracts as graphs
---
# Contracts as graphs: one Series A, clause by clause

A round is not one document. The term sheet is a short map; the long-form documents it turns into are where the rights live; the cap table is what they produce. Read one at a time, they hide how they depend on each other. Read as a graph, a clause in the term sheet links to the article it becomes, to the number it changes in the cap table, and to the arguments about it.

This is one fictional round, built that way: {{ contracts.counts }}.

{{ contracts.graph }}

## The documents

{{ contracts.documents }}

## What changed between v1 and v2

The lead investor's first draft and the agreed draft differ in the clauses below. Each change links to the clause, and the [cap table](/contracts/cap-table.html) computes what each one is worth.

{{ contracts.changes }}

## Caveats {#caveats}

{{ contracts.caveats }}

## Why as a graph

- **A term sheet clause is a promise about a later document.** Following the edge from "liquidation preference" to the article that implements it is how you check the promise was kept.
- **Control sits in more than one place.** The board clause, the consent matters, the drag-along and the leaver terms each move it; only together do they say who runs the company.
- **Versions are part of the record.** What changed, when, and why is what a founder and an investor will each want to see again, years later.
- **The arguments are linked, not repeated.** Where the newsroom has argued about a clause, the clause links to the argument, such as [sell, don't issue](https://newsroom.sgit.ai/articles/sell-dont-issue.html) and [the exit is when you sell control](https://newsroom.sgit.ai/articles/the-exit-is-when-you-sell-control.html).

The [legal on demand for startups](https://newsroom.sgit.ai/articles/legal-on-demand-for-startups.html) article describes where this goes: agent teams that do the reading, lawyers who sign, and a founder's desk, an investor's desk and a deal room as vaults.

## What this does not claim

- **The documents are summaries,** written for this example. They show the shape of each clause and how the clauses connect, not the drafting.
- **One round, one jurisdiction.** Seed instruments such as advance subscription agreements, later rounds, and other countries' documents are not modelled yet.
- **The graph is drawn from a data file,** [/data/contracts.json](/data/contracts.json), by the build. A real round would need its documents parsed into that shape; that step is not built.
