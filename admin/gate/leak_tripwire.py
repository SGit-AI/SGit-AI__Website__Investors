# The leak tripwire: scans the files git would commit for credential shapes and for the secret
# part of every key held locally in .credentials/ (which is gitignored and never committed).
# Run: python3 -m admin.gate.leak_tripwire   (exit code 1 on any finding)

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Leak_Tripwire:

    PATTERNS = [('private key block'    , re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
                ('AWS access key id'    , re.compile(r'\b(AKIA|ASIA)[0-9A-Z]{16}\b')),
                ('GitHub token'         , re.compile(r'\b(gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b')),
                ('Slack token'          , re.compile(r'\bxox[abprs]-[A-Za-z0-9-]{10,}\b')),
                ('Model provider key'   , re.compile(r'\bsk-(ant-|proj-)?[A-Za-z0-9_-]{24,}\b')),
                ('Google API key'       , re.compile(r'\bAIza[0-9A-Za-z_-]{35}\b')),
                ('Assigned secret value', re.compile(r'(?i)\b(secret|password|passwd|token|api[_-]?key)\s*[:=]\s*["\'][^"\'\s]{16,}["\']'))]
    CREDENTIALS = '.credentials'
    MIN_SECRET  = 16

    def __init__(self, root=ROOT):
        self.root = root

    def files(self):
        try:
            out = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                                 cwd=self.root, capture_output=True, text=True, check=True).stdout
            return sorted(name for name in out.split('\0') if name)
        except (OSError, subprocess.CalledProcessError):                  # not a git checkout: walk the tree
            found = []
            for folder, dirs, names in os.walk(self.root):
                dirs[:] = [d for d in dirs if d not in ('.git', self.CREDENTIALS, '_site', '__pycache__')]
                found += [os.path.relpath(os.path.join(folder, name), self.root) for name in names]
            return sorted(found)

    def local_secrets(self):
        secrets = set()
        base = os.path.join(self.root, self.CREDENTIALS)
        if os.path.isdir(base):
            for folder, _, names in os.walk(base):
                for name in names:
                    for line in open(os.path.join(folder, name), encoding='utf-8', errors='ignore'):
                        for token in re.split(r'[\s:=,"\']+', line):
                            if len(token) >= self.MIN_SECRET:
                                secrets.add(token)
        return secrets

    def scan(self):
        findings = []
        secrets  = self.local_secrets()
        for name in self.files():
            if name.startswith(self.CREDENTIALS + '/'):
                findings.append((name, 0, 'file inside the credentials tier is not ignored'))
                continue
            path = os.path.join(self.root, name)
            if not os.path.isfile(path):
                continue
            try:
                text = open(path, encoding='utf-8').read()
            except UnicodeDecodeError:
                continue
            for number, line in enumerate(text.split('\n'), start=1):
                for label, pattern in self.PATTERNS:
                    if pattern.search(line):
                        findings.append((name, number, label))
                for secret in secrets:
                    if secret in line:
                        findings.append((name, number, 'secret held in .credentials/'))
        return findings


if __name__ == '__main__':
    findings = Leak_Tripwire().scan()
    for name, number, label in findings:
        print(f'LEAK {name}:{number}: {label}')
    print(f'leak tripwire: {len(findings)} finding(s)')
    sys.exit(1 if findings else 0)
