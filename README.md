# investor.sgit.ai

A website for investors and founders, angel to Series A, where they use the sgit project's tools rather than read about them. Built from [the brief](briefs/2026-10-29__article__investor-sgit-ai.md) and [the build brief](briefs/2026-10-29__build-brief__investor-sgit-ai.md) of 29 October 2026, to sgit.ai's [guidance for every repository](https://sgit.ai/docs/guidance/repositories.md).

**Status:** first version. What exists is in [REALITY.md](REALITY.md); where the brief was wrong or changed, [BRIEF-CORRECTIONS.md](BRIEF-CORRECTIONS.md).

## Run it

Python 3.12+ and Node 20+; nothing to install.

```bash
python3 -m admin.build.build_site
```

```bash
python3 -m admin.gate.site_gate
```

```bash
python3 -m unittest discover -s tests -t .
```

```bash
python3 -m http.server 8000 -d _site
```

## Where things are

| Path | What it holds |
|---|---|
| `briefs/` | The brief, published in full, never edited |
| `content/pages/` | The pages, in Markdown with a small front matter; `{{ slot }}` markers pull in computed parts |
| `content/data/` | The data behind the computed parts: the contracts graph, the framework, the news ledger |
| `admin/build/` | The build: Markdown to HTML and `.md` twins, the generated pages, the round arithmetic |
| `admin/gate/` | The gate that fails the build, and the leak tripwire |
| `site/` | CSS, the shared JavaScript and the web components (three files each) |
| `team/` | Roles, behaviour policy, the board and the append lane |
| `review/intent/` | The project's intent, from the brief |
| `tests/` | Tests against the real build, with a negative control for each gate check |
| `version` | Written only by CI. Do not edit it |

## Versions

CI owns the version ([why](https://newsroom.sgit.ai/articles/ci-owns-the-version.html)). Commit without a number in the subject; a push to `dev` that passes the gate is released as the next patch version, a merge to `main` as the next minor. The release job stamps `version`, rebuilds, tags, deploys to GitHub Pages and checks that the live site serves the new version.

## Licences

Code Apache-2.0 ([LICENSE](LICENSE)); content CC BY 4.0. The evaluation framework is by Dinis Cruz, CC BY 4.0.
