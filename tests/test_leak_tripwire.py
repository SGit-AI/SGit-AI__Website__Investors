import os
import shutil
import tempfile
import unittest

from admin.gate.leak_tripwire import Leak_Tripwire, ROOT

# planted values are assembled at run time so this file does not trip the scan itself
AWS_KEY = 'AKIA' + 'Z' * 16
PEM     = '-----BEGIN ' + 'PRIVATE KEY-----'
SECRET  = 'vault-key-' + 'q7' * 12


class test_Leak_Tripwire(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w').write(text)

    def test_clean_tree_has_no_findings(self):
        self.write('page.md', 'Read keys may be published; vault keys never.')
        self.assertEqual(Leak_Tripwire(self.root).scan(), [])

    def test_catches_credential_shapes(self):
        self.write('a.txt', f'key = {AWS_KEY}')
        self.write('b.txt', PEM)
        labels = [label for _, _, label in Leak_Tripwire(self.root).scan()]
        self.assertIn('AWS access key id', labels)
        self.assertIn('private key block', labels)

    def test_catches_a_locally_held_secret_anywhere(self):                     # a shape no pattern knows, found because it is held locally
        self.write('.credentials/vault.txt', f'write_key: {SECRET}')
        self.write('notes/log.md', f'debug output {SECRET} end')
        findings = Leak_Tripwire(self.root).scan()
        self.assertIn(('notes/log.md', 1, 'secret held in .credentials/'), findings)

    def test_this_repository_is_clean(self):
        self.assertEqual(Leak_Tripwire(ROOT).scan(), [])
