# Builds the real site into a temporary folder and runs the real gate on it,
# with a negative control for each check: break the build, and the gate must fail.

import json
import os
import shutil
import tempfile
import unittest

from admin.build.build_site import Build_Site, ROOT
from admin.gate.site_gate   import Site_Gate


class test_Site(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.mkdtemp()
        cls.out  = os.path.join(cls.temp, 'site')
        cls.site = Build_Site(out=cls.out).build()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp)

    def copy(self):
        target = os.path.join(tempfile.mkdtemp(dir=self.temp), 'site')
        shutil.copytree(self.out, target)
        return target

    def gate(self, folder):
        return Site_Gate(folder).run(leaks=False)

    def edit(self, folder, rel, old, new):
        path = os.path.join(folder, rel)
        text = open(path, encoding='utf-8').read()
        self.assertIn(old, text)
        open(path, 'w', encoding='utf-8').write(text.replace(old, new, 1))

    def test_the_built_site_passes_the_gate(self):
        self.assertEqual(self.gate(self.out).failures, [])

    def test_build_is_deterministic(self):
        again = Build_Site(out=os.path.join(self.temp, 'again')).build()
        for folder, _, names in os.walk(self.out):
            for name in names:
                rel = os.path.relpath(os.path.join(folder, name), self.out)
                self.assertEqual(open(os.path.join(self.out, rel), 'rb').read(), open(os.path.join(again.out, rel), 'rb').read(), rel)

    def test_counts_come_from_the_data(self):
        data    = json.load(open(os.path.join(ROOT, 'content', 'data', 'contracts.json')))
        clauses = [c for d in data['documents'] for c in d['clauses']]
        changed = [c for c in clauses if isinstance(c['text'], dict)]
        page    = open(os.path.join(self.out, 'contracts', 'index.html'), encoding='utf-8').read()
        self.assertIn(f'{len(clauses)} clauses', page)
        self.assertIn(f'{len(changed)} clauses changed', page)

    def test_every_page_has_a_twin_listed_in_llms_txt(self):
        llms = open(os.path.join(self.out, 'llms.txt')).read()
        for page in self.site.pages:
            self.assertTrue(os.path.exists(os.path.join(self.out, page.path + '.md')))
            if page.path != '404':
                self.assertIn(f']({page.path}.md)', llms)

    # ---- negative controls: each check must catch a planted fault ----

    def test_gate_catches_a_broken_link(self):
        folder = self.copy()
        self.edit(folder, 'index.html', 'href="news/index.html"', 'href="news/missing.html"')
        self.assertIn('links', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_a_missing_anchor(self):
        folder = self.copy()
        self.edit(folder, 'contracts/term-sheet.html', 'id="ts-pool"', 'id="ts-pool-gone"')
        self.assertIn('anchors', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_an_orphan(self):
        folder = self.copy()
        shutil.copyfile(os.path.join(folder, 'feedback', 'index.html'), os.path.join(folder, 'lonely.html'))
        shutil.copyfile(os.path.join(folder, 'feedback', 'index.md'  ), os.path.join(folder, 'lonely.md'))
        self.assertIn('orphans', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_an_external_resource(self):
        folder = self.copy()
        self.edit(folder, 'index.html', '</head>', '<script src="https://cdn.example.com/x.js"></script></head>')
        self.assertIn('external', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_a_missing_twin(self):
        folder = self.copy()
        os.remove(os.path.join(folder, 'keys', 'index.md'))
        self.assertIn('twins', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_a_wrong_version(self):
        folder = self.copy()
        self.edit(folder, 'index.html', f'investor.sgit.ai {self.site.version}"', 'investor.sgit.ai v9.9.9"')
        self.assertIn('version', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_an_em_dash(self):
        folder = self.copy()
        self.edit(folder, 'feedback/index.html', 'This site exists', 'This site — exists')
        self.assertIn('em-dash', [check for check, _ in self.gate(folder).failures])

    def test_gate_catches_a_script_that_does_not_parse(self):
        folder = self.copy()
        with open(os.path.join(folder, 'lib', 'round-maths.js'), 'a') as handle:
            handle.write('\nexport const broken = {\n')
        self.assertIn('scripts', [check for check, _ in self.gate(folder).failures])
