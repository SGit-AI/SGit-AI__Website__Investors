# Reality: what exists in investors.sgit.ai

A feature that is not in this file does not exist. Kept current by whoever ships. Last updated: 29 October 2026, first version.

## The site

| Domain | Exists | Does not exist yet |
|---|---|---|
| Build | `admin/build/`: stdlib Python, builds 21 pages, each with a `.md` twin, plus `llms.txt`, `version.txt`, `/data/*.json`, `/briefs/*.md`. Deterministic (tested) | A sitemap; a 404 page that works at any depth (links on it are relative to the root) |
| Home | Sections table computed from page front matter | |
| 1. The news | Page, item rules, graph schema, empty ledger (`content/data/news.json`, 0 items) | Any item; the wire; the decision on who writes it (board 001) |
| 2. Contracts as graphs | One fictional Series A: 5 documents, 29 clauses, term sheet v1 and v2; clause graph as SVG; one page per document with edges and backlinks; cap table and exit waterfall computed by the build; round modeller in the browser | Parsing real documents into the graph; seed instruments; other jurisdictions; more than one preferred class |
| 3. For founders | Talking to investors, the steps of a round, help that exists, funding models table | Services directory; anything founder-specific that runs |
| 4. Evaluation framework | Criteria and bands from the March 2026 source as data; scorecard in the browser (nothing stored or sent) | Any company scored in public; maturity levels |
| 5 to 8 | A page each, marked proposed | Deal rooms, keys, the case study material, RiskMandate at work |
| Feedback | A page with the question and the address | A way to record answers on the site |

## Engineering

| Domain | Exists | Does not exist yet |
|---|---|---|
| Gate | `admin/gate/site_gate.py`: links and anchors resolve, no orphans, twins and `llms.txt`, no external resources, version on every page, no unfilled slots, no em-dashes, scripts parse (node), data parses, leak tripwire; advisory on absolutes | Code-style checks from coding.sgit.ai; freshness of `review/` |
| Tests | 26 tests: build, gate with a negative control per check, round arithmetic in Python and JavaScript against each other, Markdown, tripwire with planted keys | Browser tests in CI (run by hand with Playwright for this version) |
| Version | `version` file, written by CI only; guard in the release job | Any release: no tag exists yet |
| Release and deploy | `.github/workflows/site.yml`: validate, release (numbers, tags, pushes), deploy to Pages, verify live | Has not run on `dev` or `main`. Needs Pages set to "GitHub Actions" |
| Credentials | `.credentials/` gitignored; tripwire scans tracked and untracked files and every secret held there | sgit vault key shapes in the patterns |
| Review | `review/intent/` from the brief | Code graph, join, navigator, `review/self/` |
| Team | Roles, behaviour policy, board, inbox as files | Any agent running on a schedule; agents' published keys |
| Domain | | DNS and Pages custom domain for investors.sgit.ai |
