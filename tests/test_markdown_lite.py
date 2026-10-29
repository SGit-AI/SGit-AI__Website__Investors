import unittest

from admin.build.markdown_lite import Markdown_Lite


class test_Markdown_Lite(unittest.TestCase):

    def setUp(self):
        self.md = Markdown_Lite(link_resolver=lambda href: href.replace('/', 'X/', 1) if href.startswith('/') else href)

    def test_headings_get_ids(self):
        self.assertEqual(self.md.to_html('## The pool {#cap-pool}'), '<h2 id="cap-pool">The pool</h2>')
        self.assertEqual(self.md.to_html('# Use it, don\'t read'), '<h1 id="use-it-don-t-read">Use it, don\'t read</h1>')

    def test_inline(self):
        self.assertEqual(self.md.to_html('**a** *b* `c<d` [e](/f.html)'),
                         '<p><strong>a</strong> <em>b</em> <code>c&lt;d</code> <a href="X/f.html">e</a></p>')

    def test_lists_and_tables(self):
        self.assertEqual(self.md.to_html('- one\n- two'), '<ul><li>one</li><li>two</li></ul>')
        self.assertEqual(self.md.to_html('1. one\n2. two'), '<ol><li>one</li><li>two</li></ol>')
        html = self.md.to_html('| a | b |\n|---|---|\n| 1 | 2 |')
        self.assertIn('<th>a</th><th>b</th>', html)
        self.assertIn('<td>1</td><td>2</td>', html)

    def test_raw_html_passes_through_and_leaves_a_note_in_the_twin(self):
        text = 'Before\n\n<widget data-twin-note="Runs on the page.">x</widget>\n\nAfter'
        self.assertIn('<widget data-twin-note="Runs on the page.">x</widget>', self.md.to_html(text))
        self.assertEqual(self.md.to_twin(text), 'Before\n\n*Runs on the page.*\n\nAfter')

    def test_escapes_text(self):
        self.assertEqual(self.md.to_html('a < b & c'), '<p>a &lt; b &amp; c</p>')
