# The gate: fails the build if the built site breaks a rule. Run after the build.
# Run: python3 -m admin.gate.site_gate [site_dir]   (exit code 1 on any failure)

import html
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile

from admin.gate.leak_tripwire import Leak_Tripwire

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Site_Gate:

    RE_REF       = re.compile(r'\b(href|src)="([^"]*)"')
    RE_ID        = re.compile(r'\bid="([^"]+)"')
    RE_EXTERNAL  = re.compile(r'<(link|script|img|iframe)\b[^>]*\b(href|src)="(https?:)?//', re.I)
    RE_SCRIPT    = re.compile(r'<script\b[^>]*>(.*?)</script>', re.S)
    ABSOLUTES    = re.compile(r'\b(always|never|impossible|nobody|guarantee[sd]?|completely safe)\b', re.I)
    NO_ORPHAN_OK = {'index.html', '404.html'}
    FRAGMENTS    = 'components/'                                       # a component's markup is a fragment, not a page

    def __init__(self, site_dir=None, root=ROOT):
        self.root     = root
        self.site     = site_dir or os.path.join(root, '_site')
        self.failures = []
        self.advisory = []
        self.version  = open(os.path.join(root, 'version')).read().strip()

    def fail(self, check, message):
        self.failures.append((check, message))

    def html_files(self):
        out = []
        for folder, _, names in os.walk(self.site):
            out += [posixpath.relpath(os.path.join(folder, n), self.site).replace(os.sep, '/') for n in names if n.endswith('.html')]
        return sorted(rel for rel in out if not rel.startswith(self.FRAGMENTS))

    def read(self, rel):
        return open(os.path.join(self.site, rel), encoding='utf-8').read()

    def visible_text(self, page):
        page = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', page, flags=re.S)
        return html.unescape(re.sub(r'<[^>]+>', ' ', page))

    # ---- checks ----

    def check_links(self, pages):
        ids, linked = {}, set()
        for rel in pages:
            ids[rel] = set(self.RE_ID.findall(self.read(rel)))
        for rel in pages:
            for _, ref in self.RE_REF.findall(self.read(rel)):
                ref = html.unescape(ref)
                if ref.startswith(('http://', 'https://', 'mailto:')) or ref == '':
                    continue
                target, _, anchor = ref.partition('#')
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target)) if target else rel
                if resolved.startswith('..') or not os.path.exists(os.path.join(self.site, resolved)):
                    self.fail('links', f'{rel}: {ref} does not resolve')
                    continue
                if resolved != rel:
                    linked.add(resolved)
                if anchor and resolved.endswith('.html') and anchor not in ids.get(resolved, set()):
                    self.fail('anchors', f'{rel}: {ref} has no element with id "{anchor}"')
        for rel in pages:
            if rel not in linked and rel not in self.NO_ORPHAN_OK:
                self.fail('orphans', f'{rel}: no page links to it')

    def check_external(self, pages):
        for rel in pages:
            for match in self.RE_EXTERNAL.finditer(self.read(rel)):
                self.fail('external', f'{rel}: loads a resource from outside the site: {match.group(0)[:80]}')

    def check_twins(self, pages):
        llms = self.read('llms.txt') if os.path.exists(os.path.join(self.site, 'llms.txt')) else ''
        if not llms:
            self.fail('twins', 'llms.txt is missing')
        for rel in pages:
            twin = rel[:-5] + '.md'
            if not os.path.exists(os.path.join(self.site, twin)):
                self.fail('twins', f'{rel}: no .md twin')
            if rel != '404.html' and f']({twin})' not in llms:
                self.fail('twins', f'{rel}: not listed in llms.txt')

    def check_version(self, pages):
        stamp = f'<meta name="generator" content="investor.sgit.ai {self.version}">'
        for rel in pages:
            if stamp not in self.read(rel):
                self.fail('version', f'{rel}: does not carry version {self.version}')
        served = os.path.join(self.site, 'version.txt')
        if not os.path.exists(served) or open(served).read().strip() != self.version:
            self.fail('version', 'version.txt does not match the version file')

    def check_slots(self, pages):
        twins = [p[:-5] + '.md' for p in pages if os.path.exists(os.path.join(self.site, p[:-5] + '.md'))]
        for rel in pages + twins:
            if '{{' in self.read(rel):
                self.fail('slots', f'{rel}: an unfilled {{{{ slot }}}}')

    def check_prose(self, pages):
        for rel in pages:
            text = self.visible_text(self.read(rel))
            if '—' in text:
                self.fail('em-dash', f'{rel}: an em-dash in prose')
            for match in self.ABSOLUTES.finditer(text):
                self.advisory.append(f'{rel}: "{match.group(0)}"')

    def check_scripts(self, pages):
        node = shutil.which('node')
        if not node:
            self.fail('scripts', 'node is not installed, so scripts cannot be parse-checked')
            return
        scripts = []
        for folder, _, names in os.walk(self.site):
            scripts += [os.path.join(folder, n) for n in names if n.endswith('.js')]
        with tempfile.TemporaryDirectory() as temp:
            for rel in pages:
                for n, body in enumerate(self.RE_SCRIPT.findall(self.read(rel))):
                    if body.strip():
                        path = os.path.join(temp, f'{rel.replace("/", "__")}__{n}.mjs')
                        open(path, 'w').write(body)
                        scripts.append(path)
            for script in sorted(scripts):
                source = open(script, encoding='utf-8').read()
                result = subprocess.run([node, '--input-type=module', '--check'], input=source, capture_output=True, text=True)
                if result.returncode != 0:
                    self.fail('scripts', f'{os.path.relpath(script, self.site)}: {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "does not parse"}')

    def check_data(self):
        data = os.path.join(self.site, 'data')
        for name in sorted(os.listdir(data)) if os.path.isdir(data) else []:
            try:
                json.load(open(os.path.join(data, name)))
            except ValueError as error:
                self.fail('data', f'data/{name}: {error}')

    def check_leaks(self):
        for name, number, label in Leak_Tripwire(self.root).scan():
            self.fail('leaks', f'{name}:{number}: {label}')

    def run(self, leaks=True):
        pages = self.html_files()
        if not pages:
            self.fail('build', f'no pages in {self.site}; run the build first')
            return self
        self.check_links(pages)
        self.check_external(pages)
        self.check_twins(pages)
        self.check_version(pages)
        self.check_slots(pages)
        self.check_prose(pages)
        self.check_scripts(pages)
        self.check_data()
        if leaks:
            self.check_leaks()
        return self


if __name__ == '__main__':
    gate = Site_Gate(sys.argv[1] if len(sys.argv) > 1 else None).run()
    for line in gate.advisory:
        print(f'advisory  {line}')
    for check, message in gate.failures:
        print(f'FAIL {check:9} {message}')
    print(f'gate: {len(gate.failures)} failure(s), {len(gate.advisory)} advisory note(s)')
    sys.exit(1 if gate.failures else 0)
