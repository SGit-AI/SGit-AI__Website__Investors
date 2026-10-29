# For agents working in this repository

1. Read `REALITY.md` first. A feature that is not in it does not exist.
2. Read `team/README.md` and the role you are playing in `team/roles/`.
3. Never edit `version`, and never put a version number in a commit subject. CI owns the version.
4. Before every push: `python3 -m admin.build.build_site && python3 -m admin.gate.site_gate && python3 -m unittest discover -s tests -t .`
5. Never edit `briefs/`. Where the brief is wrong, add an entry to `BRIEF-CORRECTIONS.md`.
6. No em-dashes in prose; state the status of everything; every number on a page is computed from data, not typed.
7. Code follows coding.sgit.ai: classes not module-level functions in Python; web components as three files on `site/components/base/base-component.js`; every colour a token in `site/assets/site.css`.
8. Read keys may be published; vault keys never. Credentials only in `.credentials/` (gitignored, scanned by the tripwire).
