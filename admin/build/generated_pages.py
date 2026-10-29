# The parts of the site computed from content/data: the contracts graph and its documents,
# the cap tables and waterfalls, the framework, the news ledger and the release history.
# Content pages pull these in through {{ slot }} markers; the document pages are generated whole.

import html
import json
import os
import re

from admin.build.round_maths import Round_Maths

NEWSROOM = 'https://newsroom.sgit.ai/articles/'


class Generated_Pages:

    def __init__(self, site):
        self.site      = site
        self.contracts = site.data.get('contracts', {})
        self.framework = site.data.get('framework', {})
        self.news      = site.data.get('news', {})
        self.maths     = Round_Maths()
        self.clauses   = {}                                              # clause id -> (document, clause)
        for document in self.contracts.get('documents', []):
            for clause in document['clauses']:
                self.clauses[clause['id']] = (document, clause)

    # ---- shared helpers ----

    def money(self, value):
        return f'£{value:,.0f}'

    def pct(self, value):
        return f'{value * 100:.2f}%'

    def clause_href(self, clause_id):
        document, _ = self.clauses[clause_id]
        return f'/contracts/{document.get("page", document["id"])}.html#{clause_id}'

    def clause_label(self, clause_id):
        document, clause = self.clauses[clause_id]
        return f'{document["title"]}: {clause["title"]}'

    def backlinks(self):
        back = {}
        for document in self.contracts.get('documents', []):
            for clause in document['clauses']:
                for link in clause.get('links', []):
                    back.setdefault(link['to'], []).append((clause['id'], link['rel']))
        return back

    def versions(self):
        return [version['id'] for version in self.contracts.get('versions', [])]

    def changed_clauses(self):
        return [clause for _, clause in self.clauses.values() if isinstance(clause.get('text'), dict)]

    def rounds(self):
        cap = self.contracts['cap_table']
        out = {}
        for version, terms in self.contracts['rounds'].items():
            out[version] = self.maths.priced_round(cap['holders'], cap['existing_pool'], terms['investment'],
                                                   terms['pre_money'], terms['pool_pct'], terms['pool_in_pre_money'])
        return out

    # ---- slots ----

    def slot(self, name, page):
        handlers = { 'version'              : lambda: self.site.version,
                     'sections.table'       : self.sections_table,
                     'contracts.graph'      : self.contracts_graph,
                     'contracts.documents'  : self.contracts_documents,
                     'contracts.changes'    : self.contracts_changes,
                     'contracts.caveats'    : self.contracts_caveats,
                     'contracts.counts'     : self.contracts_counts,
                     'cap.terms'            : self.cap_terms,
                     'cap.tables'           : self.cap_tables,
                     'cap.waterfall'        : self.cap_waterfall,
                     'cap.founders_delta'   : self.cap_founders_delta,
                     'cap.modeller'         : self.cap_modeller,
                     'framework.criteria'   : self.framework_criteria,
                     'framework.bands'      : self.framework_bands,
                     'framework.scorecard'  : self.framework_scorecard,
                     'framework.not'        : self.framework_not,
                     'news.ledger'          : self.news_ledger,
                     'news.schema'          : self.news_schema,
                     'releases.list'        : self.releases_list,
                     'team.roles'           : self.team_roles,
                     'team.board'           : self.team_board }
        if name not in handlers:
            raise KeyError(f'unknown slot {{{{ {name} }}}} in {page.path}')
        return handlers[name]()

    # ---- home ----

    def sections_table(self):
        rows = ['| # | Section | Status | What it holds |', '|---|---|---|---|']
        for number, page in enumerate(self.section_pages(), start=1):
            label = { 'first': 'First version', 'empty': 'Built, empty', 'proposed': 'Proposed', 'live': 'Live' }.get(page.status, page.status)
            rows.append(f'| {number} | [{page.meta.get("short", page.title)}](/{page.path}.html) | {label} | {page.description} |')
        return '\n'.join(rows)

    def section_pages(self):
        pages = [page for page in self.site.pages if page.meta.get('order')]
        return sorted(pages, key=lambda page: int(page.meta['order']))

    # ---- contracts ----

    def contracts_counts(self):
        edges = sum(len(clause.get('links', [])) + len(clause.get('argued_in', [])) for _, clause in self.clauses.values())
        return (f'{len(self.contracts["documents"])} documents, {len(self.clauses)} clauses, {edges} links between them, '
                f'{len(self.versions())} versions of the term sheet and {len(self.changed_clauses())} clauses changed between them')

    def contracts_caveats(self):
        return '\n'.join(f'- {caveat}' for caveat in self.contracts['caveats'])

    def contracts_documents(self):
        rows = ['| Document | Clauses | What it is |', '|---|---|---|']
        for document in self.contracts['documents']:
            rows.append(f'| [{document["title"]}](/contracts/{document.get("page", document["id"])}.html) | {len(document["clauses"])} | {document["summary"]} |')
        return '\n'.join(rows)

    def contracts_changes(self):
        versions = self.contracts['versions']
        first, last = versions[0]['id'], versions[-1]['id']
        rows = [f'| Clause | {first} ({versions[0]["date"]}) | {last} ({versions[-1]["date"]}) | Why it changed |', '|---|---|---|---|']
        for clause in self.changed_clauses():
            rows.append(f'| [{clause["title"]}]({self.clause_href(clause["id"])}) | {clause["text"][first]} | {clause["text"][last]} | {clause.get("change", "")} |')
        return '\n'.join(rows)

    def document_page(self, document):
        from admin.build.build_site import Page
        back  = self.backlinks()
        lines = [f'# {document["title"]}', '', document['summary'], '',
                 f'Part of [one fictional Series A, as a graph](/contracts/index.html): {self.contracts["company"]["name"]}. '
                 f'Read [the caveats](/contracts/index.html#caveats) first.', '']
        if document.get('versioned'):
            lines += ['| Version | Date | Note |', '|---|---|---|']
            lines += [f'| {v["id"]} | {v["date"]} | {v["note"]} |' for v in self.contracts['versions']]
            lines += ['', f'Clauses that changed between versions: {len(self.changed_clauses())}. [Compare them side by side](/contracts/index.html#what-changed-between-v1-and-v2).', '']
        lines += ['## Clauses', '']
        lines += [f'{n}. [{clause["title"]}](#{clause["id"]})' for n, clause in enumerate(document['clauses'], start=1)]
        lines.append('')
        for clause in document['clauses']:
            lines += self.clause_section(clause, back)
        page = Page(f'contracts/{document["id"]}', { 'title'      : f'{document["title"]}, the example Series A',
                                                     'description': document['summary'],
                                                     'status'     : 'first' }, '\n'.join(lines))
        return page

    def clause_section(self, clause, back):
        lines = [f'### {clause["title"]} {{#{clause["id"]}}}', '']
        text  = clause['text']
        if isinstance(text, dict):
            for version in self.versions():
                lines += [f'**{version}.** {text[version]}', '']
            lines += [f'> **Changed in {self.versions()[-1]}.** {clause["change"]}', ''] if clause.get('change') else []
        else:
            lines += [text, '']
        if clause.get('caveat'):
            lines += [f'*Caveat.* {clause["caveat"]}', '']
        edges = [f'- {link["rel"]}: [{self.clause_label(link["to"])}]({self.clause_href(link["to"])})' for link in clause.get('links', [])]
        edges += [f'- linked from ({rel}): [{self.clause_label(source)}]({self.clause_href(source)})' for source, rel in back.get(clause['id'], [])]
        edges += [f'- argued in: [{self.contracts["arguments"][slug].split(":")[0]}]({NEWSROOM}{slug}.html), on newsroom.sgit.ai' for slug in clause.get('argued_in', [])]
        if edges:
            lines += ['Edges:', ''] + edges + ['']
        return lines

    def contracts_graph(self):
        columns = [('Arguments, newsroom.sgit.ai', [('argument', slug) for slug in self.contracts['arguments'] if self.argued(slug)]),
                   ('Term sheet'                 , self.doc_nodes('term-sheet')),
                   ('Agreement and option rules' , self.doc_nodes('sha') + self.doc_nodes('option-plan')),
                   ('Articles of association'    , self.doc_nodes('articles')),
                   ('Cap table'                  , self.doc_nodes('cap-table'))]
        col_w, node_w, node_h, gap, top = 188, 164, 24, 8, 40
        pos, parts = {}, []
        height = top + max(len(nodes) for _, nodes in columns) * (node_h + gap) + 20
        width  = col_w * len(columns)
        for c, (label, nodes) in enumerate(columns):
            x = c * col_w + 12
            parts.append(f'<text class="g-col" x="{x}" y="20">{html.escape(label)}</text>')
            for r, (kind, node_id) in enumerate(nodes):
                y = top + r * (node_h + gap)
                pos[node_id] = (x, y, kind)
        edges = []
        for _, clause in self.clauses.values():
            for link in clause.get('links', []):
                edges.append((clause['id'], link['to'], 'edge-' + link['rel'].replace(' ', '-')))
            for slug in clause.get('argued_in', []):
                edges.append((slug, clause['id'], 'edge-argued'))
        for source, target, css in edges:
            sx, sy, _ = pos[source]
            tx, ty, _ = pos[target]
            sy, ty = sy + node_h / 2, ty + node_h / 2
            if tx > sx:
                x1, x2 = sx + node_w, tx
                path = f'M{x1},{sy} C{x1 + 40},{sy} {x2 - 40},{ty} {x2},{ty}'
            elif tx < sx:
                x1, x2 = sx, tx + node_w
                path = f'M{x1},{sy} C{x1 - 40},{sy} {x2 + 40},{ty} {x2},{ty}'
            else:
                x1 = sx + node_w
                path = f'M{x1},{sy} C{x1 + 30},{sy} {x1 + 30},{ty} {x1},{ty}'
            parts.insert(0, f'<path class="g-edge {css}" d="{path}"/>')
        for node_id, (x, y, kind) in pos.items():
            if kind == 'argument':
                href  = f'{NEWSROOM}{node_id}.html'
                label = self.contracts['arguments'][node_id].split(':')[0]
            else:
                href  = self.clause_href(node_id)
                label = self.clauses[node_id][1]['title']
            short = label if len(label) <= 26 else label[:25] + '…'
            parts.append(f'<a href="{href}"><g class="g-node g-{kind}"><title>{html.escape(label)}</title>'
                         f'<rect x="{x}" y="{y}" width="{node_w}" height="{node_h}" rx="5"/>'
                         f'<text x="{x + 8}" y="{y + 16}">{html.escape(short)}</text></g></a>')
        note = html.escape(f'The graph is drawn on the HTML page; its {len(edges)} edges are listed clause by clause on each document page.')
        return (f'<figure class="graph" data-twin-note="{note}"><div class="graph-scroll">'
                f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="The clauses of the example Series A and the links between them">'
                + ''.join(parts) +
                '</svg></div><figcaption><span class="key key-becomes">becomes</span> <span class="key key-computed">computed in</span> '
                '<span class="key key-other">read with, defines, excludes</span> <span class="key key-argued">argued in</span> '
                '· every box is a link</figcaption></figure>')

    def argued(self, slug):
        return any(slug in clause.get('argued_in', []) for _, clause in self.clauses.values())

    def doc_nodes(self, document_id):
        for document in self.contracts['documents']:
            if document['id'] == document_id:
                return [('clause', clause['id']) for clause in document['clauses']]
        return []

    # ---- cap table ----

    def cap_terms(self):
        rows = ['| Term | ' + ' | '.join(self.versions()) + ' |', '|---|' + '---|' * len(self.versions())]
        terms = self.contracts['rounds']
        def row(label, fn):
            return f'| {label} | ' + ' | '.join(fn(terms[v]) for v in self.versions()) + ' |'
        rows += [row('Investment'          , lambda t: self.money(t['investment'])),
                 row('Pre-money valuation' , lambda t: self.money(t['pre_money'])),
                 row('Option pool, share of the company after the round', lambda t: f'{t["pool_pct"] * 100:g}%'),
                 row('Pool counted in'     , lambda t: 'pre-money' if t['pool_in_pre_money'] else 'post-money'),
                 row('Liquidation preference', lambda t: f'{t["preference_multiple"]}x ' + ('participating' if t['participating'] else 'non-participating'))]
        return '\n'.join(rows)

    def cap_tables(self):
        rounds = self.rounds()
        out    = []
        for version in self.versions():
            result = rounds[version]
            out += [f'### Cap table after the round, term sheet {version} {{#cap-table-{version}}}', '',
                    f'Price per share £{result["price"]:.4f}; {result["new_shares"]:,} new Series A shares; '
                    f'{result["new_pool"]:,} new pool shares; {result["post_shares"]:,} shares after the round; post-money valuation {self.money(result["post_money"])}.', '',
                    '| Holder | Class | Before | % before | After | % after |', '|---|---|---|---|---|---|']
            for row in result['rows']:
                out.append(f'| {row["name"]} | {row["class"]} | {row["pre"]:,} | {self.pct(row["pre_pct"])} | {row["post"]:,} | {self.pct(row["post_pct"])} |')
            out.append('')
        return '\n'.join(out)

    def cap_founders_delta(self):
        rounds  = self.rounds()
        first, last = self.versions()[0], self.versions()[-1]
        share   = lambda version: sum(row['post_pct'] for row in rounds[version]['rows'] if row['id'].startswith('founder'))
        delta   = share(last) - share(first)
        return (f'The founders together hold {self.pct(share(first))} after the round under {first} and {self.pct(share(last))} under {last}: '
                f'a difference of {delta * 100:.2f} percentage points, from the smaller pool alone.')

    def cap_waterfall(self):
        rounds = self.rounds()
        cap    = self.contracts['cap_table']
        out    = []
        for version in self.versions():
            terms = self.contracts['rounds'][version]
            kind  = 'participating' if terms['participating'] else 'non-participating'
            out  += [f'### Exit waterfall, term sheet {version}: {terms["preference_multiple"]}x {kind} {{#waterfall-{version}}}', '']
            names = [row['name'] for row in rounds[version]['rows']]
            out  += ['| Exit value | ' + ' | '.join(names) + ' |', '|---|' + '---|' * len(names)]
            for exit_value in cap['exit_values']:
                result = self.maths.waterfall(rounds[version], terms['investment'], terms['preference_multiple'], terms['participating'], exit_value)
                cells  = [self.money(result['payout'][row['id']]) for row in rounds[version]['rows']]
                mark   = ' (Series A converts)' if result['converts'] else ''
                out.append(f'| {self.money(exit_value)}{mark} | ' + ' | '.join(cells) + ' |')
            out.append('')
        return '\n'.join(out)

    def cap_modeller(self):
        cap   = self.contracts['cap_table']
        terms = self.contracts['rounds'][self.versions()[-1]]
        data  = html.escape(json.dumps({ 'holders': cap['holders'], 'existing_pool': cap['existing_pool'], 'terms': terms }, sort_keys=True))
        note  = html.escape('The round modeller runs on the HTML page: change the terms and the cap table and waterfall recompute in the browser.')
        return (f'<round-modeller data-model="{data}" data-twin-note="{note}"><p>The round modeller needs JavaScript; the tables below are the same arithmetic, computed by the build.</p></round-modeller>\n'
                '<script type="module" src="/components/round-modeller/round-modeller.js"></script>')

    # ---- framework ----

    def framework_criteria(self):
        out = []
        for criterion in self.framework['criteria']:
            star = ' One of the two the framework names as "the strongest predictors of long-term value".' if criterion['id'] in self.framework['strongest_predictors'] else ''
            out += [f'### {criterion["number"]}. {criterion["name"]}: {criterion["heading"]} {{#{criterion["id"]}}}', '',
                    f'**The question to ask:** "{criterion["question"]}"{star}', '',
                    f'- Red flag: {criterion["red"]}', f'- Green flag: {criterion["green"]}', '']
        return '\n'.join(out)

    def framework_bands(self):
        rows  = ['| Total | Band | Meaning |', '|---|---|---|']
        rows += [f'| {band["min"]} to {band["max"]} | {band["label"]} | {band["meaning"]} |' for band in self.framework['bands']]
        rows += ['', '| Score | Label | Meaning |', '|---|---|---|']
        rows += [f'| {score["score"]} | {score["label"]} | {score["meaning"]} |' for score in self.framework['scores']]
        return '\n'.join(rows)

    def framework_not(self):
        return '\n'.join(f'- {item}' for item in self.framework['not_evaluated'])

    def framework_scorecard(self):
        note = html.escape('The scorecard runs on the HTML page: score each criterion from 1 to 5 and it totals to 40 and names the band.')
        return (f'<evaluation-scorecard data-twin-note="{note}"><p>The scorecard needs JavaScript; the criteria and bands are listed below.</p></evaluation-scorecard>\n'
                '<script type="module" src="/components/evaluation-scorecard/evaluation-scorecard.js"></script>')

    # ---- news ----

    def news_ledger(self):
        items = self.news.get('items', [])
        if not items:
            return ('**Items in the ledger: 0.** The structure below is built and the first wire has not run. '
                    'Nothing is shown until it can be dated, linked and checked.')
        rows = ['| Date | What | Source |', '|---|---|---|']
        rows += [f'| {item["date"]} | {item["summary"]} | [{item["source_name"]}]({item["source_url"]}) |' for item in sorted(items, key=lambda i: i['date'], reverse=True)]
        return f'**Items in the ledger: {len(items)}.**\n\n' + '\n'.join(rows)

    def news_schema(self):
        rows  = ['| Node | What it is |', '|---|---|']
        rows += [f'| `{node["type"]}` | {node["about"]} |' for node in self.news['node_types']]
        rows += ['', '| Edge | From, to | What it says |', '|---|---|---|']
        rows += [f'| `{edge["type"]}` | {edge["from"]} to {edge["to"]} | {edge["about"]} |' for edge in self.news['edge_types']]
        return '\n'.join(rows)

    # ---- releases ----

    def releases_list(self):
        rows = self.site.releases()
        if not rows:
            return '**Releases tagged so far: 0.** The first push to `dev` that passes the gate becomes v0.0.1, numbered by CI.'
        table = ['| Version | Date | What changed |', '|---|---|---|']
        table += [f'| {tag} | {date} | {subject.replace("|", "/")} |' for tag, date, subject in rows]
        return f'**Releases tagged so far: {len(rows)}.**\n\n' + '\n'.join(table)

    # ---- team, read from team/ ----

    def team_files(self, folder):
        base = os.path.join(self.site.root, 'team', folder)
        for name in sorted(os.listdir(base)):
            if name.endswith('.md') and name != 'README.md':
                yield name, open(os.path.join(base, name), encoding='utf-8').read()

    def team_roles(self):
        rows = ['| Role | What it does |', '|---|---|']
        for _, text in self.team_files('roles'):
            title   = re.search(r'^# (.+)$', text, re.M).group(1)
            summary = text.split('\n\n')[1].strip()
            rows.append(f'| {title} | {summary} |')
        return '\n'.join(rows)

    def team_board(self):
        rows = ['| Item | Status |', '|---|---|']
        for name, text in self.team_files('board'):
            title  = re.search(r'^# (.+)$', text, re.M).group(1)
            status = re.search(r'^Status: (.+)$', text, re.M).group(1)
            rows.append(f'| {title} | {status} |')
        return '\n'.join(rows)

    # ---- generated pages ----

    def extra_pages(self):
        return [self.document_page(document) for document in self.contracts.get('documents', []) if not document.get('page')]
