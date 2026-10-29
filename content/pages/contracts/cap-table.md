---
title: The cap table and the exit waterfall, computed from the terms
description: The cap table each version of the term sheet produces, the exit waterfall under each liquidation preference, and a modeller to try your own terms.
status: first
---
# The cap table and the exit waterfall

The cap table is not a contract. It is what the contracts produce, so here it is computed from [the term sheet](/contracts/term-sheet.html), one version at a time, by the build. No number on this page is typed in.

## The terms

{{ cap.terms }}

## Who owns what after the round {#cap-round}

{{ cap.tables }}

## The pool {#cap-pool}

{{ cap.founders_delta }} That is the [option pool clause](/contracts/term-sheet.html#ts-pool) at work: with the pool counted in the pre-money valuation, every point of pool comes out of the existing shareholders' side.

## Who receives what on an exit {#cap-waterfall}

The [liquidation preference](/contracts/term-sheet.html#ts-preference) decides the order in which the proceeds of a sale are paid. The two versions differ most on a mid-sized exit.

{{ cap.waterfall }}

## Model your own round {#model-your-own-round}

Start from the agreed terms and change them. The modeller uses the same arithmetic as the tables above, written once in Python for the build and once in JavaScript for the browser; a test runs both and requires the same numbers.

{{ cap.modeller }}

## What this does not claim

- **Every option is assumed granted and exercised,** with no exercise price, no tax and no costs of the sale.
- **Seed shares are treated as ordinary shares.** In practice a seed round may carry its own preference.
- **One preferred class.** Later rounds stack preferences, and the order between them is negotiated.
