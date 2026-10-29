---
title: The news, angel to Series A, as a graph
description: What is going on in investor circles at angel and Series A, from public sources only, dated and linked, tracked as a graph so the dots connect.
status: empty
order: 1
short: The news
---
# The news, angel to Series A, as a graph

What is going on in investor circles, with the focus on the early rounds: angel, pre-seed, seed and Series A. All of it from public sources, every item dated and linked, and tracked as a semantic graph so the dots connect: who invested in whom, which funds move together, which terms are spreading.

## The ledger

{{ news.ledger }}

## The rules for an item

1. **Public sources only.** A public page, a regulator's register or a company's own announcement. Nothing from a private deck, a private message or a deal room.
2. **Dated and linked.** The date of the event, the date the source was read, and the link.
3. **Frozen and hashed.** The source is saved when it is read and its hash is kept, so a page that changes later can be compared with what we read.
4. **No private person named.** Funds, networks and companies are named. Individual angels are not, even where a source names them.
5. **Our words, their link.** One sentence of summary in our words; the source carries the detail.

## The graph

Every item adds nodes and edges, and the derived edges, such as two funds appearing in the same round, are counted from the items, never typed in.

{{ news.schema }}

The schema and the empty ledger are published as data at [/data/news.json](/data/news.json).

## Who writes the feed: an open question

The [brief](/about/brief.html) leaves one decision open. Either the [SGit Newsroom](https://newsroom.sgit.ai/) runs an investor wire, a public vault per wire that its agents write and this site reads, or this site's own team runs it.

The recommendation in the brief is the newsroom's wire, because it shows the point of vaults: one team writes, another site reads, and the vault is the contract between them. Until that is decided, this section stays empty rather than half-filled. The decision is on [the board](/about/index.html#the-board).

## What this does not claim

- **No item has been published.** The count above is read from the data file on every build.
- **The graph is a schema, not yet a graph.** It becomes one with the first items.
