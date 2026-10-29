# review/intent

The project's intent, written top down from the brief, one node per section, each carrying the brief section it comes from and its status. Written by the agent that built the first version; to be accepted by a person.

The code side (derived bottom up from the tree by a parser), the join with its coverage figure, and the navigator are not built yet. See `team/board/006__review-navigator.md`.

| Node | From the brief | Status | Built as |
|---|---|---|---|
| `news` | "The news" | built, empty | content/pages/news/index.md, content/data/news.json |
| `contracts` | "Contracts as graphs" | first version | content/data/contracts.json, admin/build/generated_pages.py, admin/build/round_maths.py, site/lib/round-maths.js, site/components/round-modeller/ |
| `founders` | "For founders", "The funding models, all of them" | first version | content/pages/founders/ |
| `framework` | "Work that got lost: the evaluation framework" | first version | content/data/framework.json, site/components/evaluation-scorecard/ |
| `deal-rooms` | "Deal rooms as vaults" | proposed | content/pages/deal-rooms/index.md |
| `keys` | "Keys for investors" | proposed | content/pages/keys/index.md |
| `case-study` | "sgit as the case study" | proposed | content/pages/case-study/index.md |
| `riskmandate` | "RiskMandate at work" | proposed | content/pages/riskmandate/index.md |
| `team` | "Run by agents, fed by the newsroom" | designed | team/ |
| `house-rules` | "Built to the house rules from the first commit" | in place, with gaps | REALITY.md, BRIEF-CORRECTIONS.md, admin/gate/, .github/workflows/site.yml |
| `ask` | "Then ask investors" | page live | content/pages/feedback/index.md |
