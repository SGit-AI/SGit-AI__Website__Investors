# The team

How investors.sgit.ai is run. A new agent reads this file and one role, then begins.

- `roles/`: one file per role, with what it does, what it may not do, and the rule behind each.
- `policies/`: the Agent Behaviour Policy each role runs under, in the shape RiskMandate gives (https://riskmandate.ai/abp.html).
- `board/`: the work, one file per item, each with a `Status:` line. The site's about page lists them on every build.
- `inbox/`: the append lane for messages and requests. One file per message, named `YYYY-MM-DD__from__subject.md`. Never edited after it is written.

The schedule is designed, not running: no agent has run here on a schedule yet (see `REALITY.md`).

Rules every role follows:

1. Read `REALITY.md` before saying anything exists.
2. Never write the version. CI owns it (`version` is written only by the release job).
3. Run the gate before every push: `python3 -m admin.gate.site_gate`.
4. Read keys may be published; vault keys never. Credentials live only in `.credentials/`, which is gitignored and scanned by the tripwire.
