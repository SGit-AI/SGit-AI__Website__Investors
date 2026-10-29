# Builds investors.sgit.ai from content/ and site/ into a static tree (default: _site/).
# Every page is written twice from the same source: the HTML page and its .md twin.
# Run: python3 -m admin.build.build_site [out_dir]

import html
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys

from admin.build.markdown_lite   import Markdown_Lite
from admin.build.generated_pages import Generated_Pages

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Page:

    def __init__(self, path, meta, body):
        self.path        = path                                          # site path without extension, e.g. 'founders/index'
        self.meta        = meta
        self.body        = body
        self.title       = meta.get('title', '')
        self.description = meta.get('description', '')
        self.status      = meta.get('status', '')
        self.section     = meta.get('section', '')


class Build_Site:

    SITE_NAME = 'investors.sgit.ai'
    NAV       = [('index'              , 'Home'        ),
                 ('news/index'         , 'The news'    ),
                 ('contracts/index'    , 'Contracts'   ),
                 ('founders/index'     , 'Founders'    ),
                 ('framework/index'    , 'Framework'   ),
                 ('deal-rooms/index'   , 'Deal rooms'  ),
                 ('keys/index'         , 'Keys'        ),
                 ('case-study/index'   , 'sgit'        ),
                 ('riskmandate/index'  , 'RiskMandate' ),
                 ('about/index'        , 'About'       )]
    STATUS    = { 'live'    : 'Live: this section runs',
                  'first'   : 'First version: built, small, and asking for feedback',
                  'empty'   : 'Built, empty: the structure runs and holds no items yet',
                  'proposed': 'Proposed: described here, not built' }
    RE_FRONT  = re.compile(r'^---\n(.*?)\n---\n', re.S)
    RE_SLOT   = re.compile(r'\{\{\s*([a-z0-9_.-]+)\s*\}\}')

    def __init__(self, root=ROOT, out=None):
        self.root      = root
        self.out       = out or os.path.join(root, '_site')
        self.version   = open(os.path.join(root, 'version')).read().strip()
        self.data      = { name[:-5]: json.load(open(os.path.join(root, 'content', 'data', name)))
                           for name in sorted(os.listdir(os.path.join(root, 'content', 'data'))) if name.endswith('.json') }
        self.generated = Generated_Pages(self)
        self.pages     = []

    # ---- loading ----

    def load_pages(self):
        base = os.path.join(self.root, 'content', 'pages')
        for folder, _, files in sorted(os.walk(base)):
            for name in sorted(files):
                if not name.endswith('.md'):
                    continue
                full = os.path.join(folder, name)
                path = os.path.relpath(full, base)[:-3].replace(os.sep, '/')
                text = open(full, encoding='utf-8').read()
                meta = {}
                front = self.RE_FRONT.match(text)
                if front:
                    for line in front.group(1).split('\n'):
                        key, _, value = line.partition(':')
                        meta[key.strip()] = value.strip()
                    text = text[front.end():]
                self.pages.append(Page(path, meta, text))
        self.pages += self.generated.extra_pages()
        self.pages.sort(key=lambda page: page.path)
        return self

    def page(self, path):
        return next(page for page in self.pages if page.path == path)

    # ---- links ----

    def relative(self, from_path, href, twin=False):
        if not href.startswith('/'):
            return href
        target, _, anchor = href[1:].partition('#')
        if twin and target.endswith('.html'):
            target = target[:-5] + '.md'
        if target == '' or target.endswith('/'):
            target += 'index.md' if twin else 'index.html'
        rel = posixpath.relpath(target, posixpath.dirname(from_path) or '.')
        return rel + (f'#{anchor}' if anchor else '')

    def fill_slots(self, page, text):
        return self.RE_SLOT.sub(lambda match: self.generated.slot(match.group(1), page), text)

    # ---- rendering ----

    def render_html(self, page, body_md):
        md        = Markdown_Lite(link_resolver=lambda href: self.relative(page.path, href))
        body_html = md.to_html(body_md)
        body_html = re.sub(r'(href|src)="(/[^"]*)"', lambda m: f'{m.group(1)}="{self.relative(page.path, m.group(2))}"', body_html)
        up        = lambda target: self.relative(page.path, '/' + target)
        nav       = ''.join(f'<li><a href="{up(path + ".html")}"{" aria-current=\"page\"" if self.nav_key(page) == path else ""}>{label}</a></li>'
                            for path, label in self.NAV)
        status    = (f'<p class="status status-{page.status}"><span>{html.escape(self.STATUS[page.status])}</span></p>'
                     if page.status in self.STATUS else '')
        twin      = posixpath.basename(page.path) + '.md'
        title     = page.title if page.path == 'index' else f'{page.title}, {self.SITE_NAME}'
        return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(page.description)}">
<meta name="generator" content="investors.sgit.ai {self.version}">
<link rel="stylesheet" href="{up('assets/site.css')}">
<link rel="alternate" type="text/markdown" href="{twin}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="bar">
    <a class="brand" href="{up('index.html')}"><span class="brand-mark" aria-hidden="true">◆</span> investors<span>.sgit.ai</span></a>
    <a class="version" href="{up('about/releases.html')}" title="Release history">{self.version}</a>
  </div>
  <nav aria-label="Sections"><ul>{nav}</ul></nav>
</header>
<main id="main">
<article>
{status}
{body_html}
</article>
</main>
<footer class="site-footer">
  <p><strong>investors.sgit.ai</strong>, for investors and founders, angel to Series A. A first version, built from <a href="{up('about/brief.html')}">the brief</a>. Is it useful? <a href="{up('feedback/index.html')}">Tell us what would help</a>.</p>
  <p><a href="{up('about/participant.html')}">Participant disclosure</a>: published by the sgit project, which builds the tools this site uses. Content CC BY 4.0, code Apache-2.0. Not investment, legal or tax advice.</p>
  <p class="meta">site {self.version} · <a href="{twin}">this page as markdown</a> · <a href="{up('llms.txt')}">llms.txt</a> · <a href="{up('about/releases.html')}">releases</a> · <a href="https://github.com/SGit-AI/SGit-AI__Website__Investors">source</a></p>
</footer>
</body>
</html>
'''

    def nav_key(self, page):
        top = page.path.split('/')[0]
        for path, _ in self.NAV:
            if path.split('/')[0] == top:
                return path
        return 'index'

    def render_twin(self, page, body_md):
        text = Markdown_Lite().to_twin(body_md)
        text = re.sub(r'\]\((/[^)\s]*)\)', lambda m: f']({self.relative(page.path, m.group(1), twin=True)})', text)
        header = (f'*Source: <https://{self.SITE_NAME}/{page.path}.html> · site {self.version} · generated from the same content as the page.*\n\n'
                  + (f'**Status:** {self.STATUS[page.status]}\n\n' if page.status in self.STATUS else ''))
        footer = f'\n\n---\n\n*[Site index for agents]({self.relative(page.path, "/llms.txt")}) · [HTML version]({posixpath.basename(page.path)}.html)*\n'
        return header + text.strip() + footer

    # ---- writing ----

    def write(self, rel_path, content):
        full = os.path.join(self.out, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(content)

    def copy_tree(self, source, target):
        source = os.path.join(self.root, source)
        for folder, _, files in sorted(os.walk(source)):
            for name in sorted(files):
                src = os.path.join(folder, name)
                dst = os.path.join(self.out, target, os.path.relpath(src, source))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)

    def llms_txt(self):
        lines = [f'# {self.SITE_NAME}', '',
                 '> A website for investors and founders, angel to Series A, that uses sgit vaults, PKI, agent teams and RiskMandate in its own working. '
                 'A first version. Every page has a .md twin; the data behind the interactive pages is in /data.', '',
                 f'Site version: {self.version}', '', '## Pages', '']
        for page in self.pages:
            if page.path == '404':
                continue
            lines.append(f'- [{page.title}]({page.path}.md): {page.description}')
        lines += ['', '## Data', '']
        lines += [f'- [{name}.json](data/{name}.json)' for name in self.data]
        lines += ['', '## The brief', '']
        lines += [f'- [{name}](briefs/{name})' for name in sorted(os.listdir(os.path.join(self.root, 'briefs'))) if name.endswith('.md')]
        return '\n'.join(lines) + '\n'

    def build(self):
        if os.path.isdir(self.out):
            shutil.rmtree(self.out)
        os.makedirs(self.out)
        self.load_pages()
        for page in self.pages:
            body = self.fill_slots(page, page.body)
            self.write(page.path + '.html', self.render_html(page, body))
            self.write(page.path + '.md'  , self.render_twin(page, body))
        self.copy_tree('site'            , '')
        self.copy_tree('briefs'          , 'briefs')
        self.copy_tree('content/data'    , 'data')
        self.write('llms.txt'   , self.llms_txt())
        self.write('version.txt', self.version + '\n')
        self.write('.nojekyll'  , '')
        return self

    # ---- release history, read from git so it is counted, not remembered ----

    def releases(self):
        try:
            out = subprocess.run(['git', 'for-each-ref', '--sort=-creatordate', '--format=%(refname:short)\t%(creatordate:short)\t%(subject)', 'refs/tags/v*'],
                                 cwd=self.root, capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            return []
        rows = []
        for line in out.strip().split('\n'):
            if line:
                tag, date, subject = line.split('\t', 2)
                subject = re.sub(r'^release v[0-9.]+:\s*', '', subject)
                rows.append((tag, date, subject))
        return rows


if __name__ == '__main__':
    site = Build_Site(out=sys.argv[1] if len(sys.argv) > 1 else None).build()
    print(f'built {len(site.pages)} pages into {site.out} at {site.version}')
