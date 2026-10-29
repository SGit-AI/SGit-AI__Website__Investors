# A small Markdown reader for this site's own content files.
# It covers what the content uses and nothing more: headings, paragraphs, lists, tables,
# blockquotes, raw HTML blocks, and inline code, bold, italics and links.
# Stdlib only, so the build fetches nothing (see BRIEF-CORRECTIONS.md, C-03).

import html
import re


class Markdown_Lite:

    RE_HEADING  = re.compile(r'^(#{1,6})\s+(.*?)(?:\s*\{#([a-z0-9-]+)\})?\s*$')
    RE_UL_ITEM  = re.compile(r'^[-*]\s+(.*)$')
    RE_OL_ITEM  = re.compile(r'^\d+\.\s+(.*)$')
    RE_TABLE    = re.compile(r'^\|.*\|\s*$')
    RE_TABLE_HR = re.compile(r'^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$')
    RE_CODE     = re.compile(r'`([^`]+)`')
    RE_LINK     = re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)')
    RE_BOLD     = re.compile(r'\*\*(.+?)\*\*')
    RE_EM       = re.compile(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])')

    def __init__(self, link_resolver=None):
        self.link_resolver = link_resolver or (lambda href: href)

    def slug(self, text):
        text = re.sub(r'<[^>]+>', '', text).lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        return text.strip('-')

    def inline(self, text):
        codes = []

        def keep_code(match):
            codes.append(match.group(1))
            return f'\x00{len(codes) - 1}\x00'

        text = self.RE_CODE.sub(keep_code, text)
        text = html.escape(text, quote=False)
        text = self.RE_LINK.sub(lambda m: f'<a href="{html.escape(self.link_resolver(m.group(2)))}">{m.group(1)}</a>', text)
        text = self.RE_BOLD.sub(r'<strong>\1</strong>', text)
        text = self.RE_EM  .sub(r'<em>\1</em>'        , text)
        text = re.sub('\x00(\\d+)\x00', lambda m: f'<code>{html.escape(codes[int(m.group(1))])}</code>', text)
        return text

    def table(self, rows):
        cells  = [[cell.strip() for cell in row.strip().strip('|').split('|')] for row in rows]
        head   = cells[0]
        body   = cells[2:] if len(cells) > 1 and self.RE_TABLE_HR.match(rows[1]) else cells[1:]
        out    = ['<div class="table-wrap"><table>', '<thead><tr>']
        out   += [f'<th>{self.inline(cell)}</th>' for cell in head]
        out   += ['</tr></thead>', '<tbody>']
        for row in body:
            out += ['<tr>'] + [f'<td>{self.inline(cell)}</td>' for cell in row] + ['</tr>']
        out   += ['</tbody></table></div>']
        return ''.join(out)

    def to_html(self, text):
        lines  = text.split('\n')
        out    = []
        i      = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if line.startswith('<'):                                        # raw HTML block, up to a blank line
                block = []
                while i < len(lines) and lines[i].strip():
                    block.append(lines[i])
                    i += 1
                out.append('\n'.join(block))
                continue
            heading = self.RE_HEADING.match(line)
            if heading:
                level, title, anchor = heading.groups()
                anchor = anchor or self.slug(title)
                out.append(f'<h{len(level)} id="{anchor}">{self.inline(title)}</h{len(level)}>')
                i += 1
                continue
            if self.RE_TABLE.match(line):
                rows = []
                while i < len(lines) and self.RE_TABLE.match(lines[i]):
                    rows.append(lines[i])
                    i += 1
                out.append(self.table(rows))
                continue
            if line.startswith('>'):
                quote = []
                while i < len(lines) and lines[i].startswith('>'):
                    quote.append(lines[i][1:].strip())
                    i += 1
                out.append(f'<blockquote><p>{self.inline(" ".join(quote))}</p></blockquote>')
                continue
            for pattern, tag in ((self.RE_UL_ITEM, 'ul'), (self.RE_OL_ITEM, 'ol')):
                if pattern.match(line):
                    items = []
                    while i < len(lines) and lines[i].strip():
                        item = pattern.match(lines[i])
                        if item:
                            items.append(item.group(1))
                        elif items:
                            items[-1] += ' ' + lines[i].strip()               # a wrapped list item
                        i += 1
                    out.append(f'<{tag}>' + ''.join(f'<li>{self.inline(item)}</li>' for item in items) + f'</{tag}>')
                    break
            else:
                para = []
                while i < len(lines) and lines[i].strip() and not self.starts_block(lines[i]):
                    para.append(lines[i].strip())
                    i += 1
                out.append(f'<p>{self.inline(" ".join(para))}</p>')
        return '\n'.join(out)

    def starts_block(self, line):
        return bool(line.startswith(('<', '>', '#')) or self.RE_TABLE.match(line)
                    or self.RE_UL_ITEM.match(line) or self.RE_OL_ITEM.match(line))

    def to_twin(self, text):                                                # the .md twin: raw HTML blocks replaced by a note
        out, skipping = [], False
        for line in text.split('\n'):
            if line.startswith('<') and not skipping:
                skipping = True
                if 'data-twin-note' in line:
                    note = re.search(r'data-twin-note="([^"]*)"', line).group(1)
                    out.append(f'*{html.unescape(note)}*')
                continue
            if skipping:
                if not line.strip():
                    skipping = False
                    out.append('')
                continue
            out.append(re.sub(r'\s*\{#[a-z0-9-]+\}\s*$', '', line))
        return '\n'.join(out)
