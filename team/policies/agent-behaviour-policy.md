# Agent Behaviour Policy: investors.sgit.ai

In the shape of RiskMandate's Agent Behaviour Policy (https://riskmandate.ai/abp.html): what each agent can reach, what it is mandated to do, the gap between the two, and the barriers in place. Status: first version, written before any agent runs on a schedule. The footprint of each run is to be read from the workflow logs and compared with this table.

| Role | Can reach | Mandated to | The gap | Barriers |
|---|---|---|---|---|
| Conductor | The repository, the board, the inbox | Assign work, open pull requests | It could write content or merge | Role file; merges to `main` by a person only |
| Journalist | The repository, public web | Write pages and ledger items | It could publish an unsourced item or a private name | The gate; the item rules on the news page; review by a second role |
| Researcher | Public web, `admin/notes/` | Read and freeze sources | It could read non-public material | Public sources only; every source dated and hashed |
| Security | The repository, the pipeline | Keep the tripwire and policies | It could weaken a check | Corrections entry required; a person reviews pipeline changes |
| Observability | The live site, workflow logs | Report on releases and runs | It could edit to hide a finding | Read-only by policy; findings go to the inbox |

Every role: no vault key in the repository, a page or a log; read keys only. Session credentials are used in the session and never written down.
