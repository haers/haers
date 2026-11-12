#!/usr/bin/env python3
"""Markdown 渲染检查：逐个核对源码标题与实际 HTML 标题。"""

from html.parser import HTMLParser
from pathlib import Path
import re

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
RENDERER = MarkdownIt('commonmark', {'html': True})


class RenderedHeadings(HTMLParser):
    """读取真实渲染出的标题，保留级别与文字顺序。"""

    def __init__(self):
        super().__init__()
        self.headings = []
        self.level = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        if re.fullmatch(r'h[1-6]', tag):
            self.level = int(tag[1])
            self.text = []

    def handle_data(self, data):
        if self.level is not None:
            self.text.append(data)

    def handle_endtag(self, tag):
        if self.level is not None and tag == f'h{self.level}':
            self.headings.append((self.level, ''.join(self.text).strip()))
            self.level = None


def check_document(text):
    """HTML 图片块后的 Markdown 标题也必须真正渲染成标题。"""
    expected = []
    for match in re.finditer(r'^(#{1,6}) (.+)$', text, re.M):
        inline = RenderedHeadings()
        level, title = len(match.group(1)), match.group(2)
        inline.feed(f'<h{level}>' + RENDERER.renderInline(title) + f'</h{level}>')
        expected.extend(inline.headings)
    actual = RenderedHeadings()
    actual.feed(RENDERER.render(text))
    if actual.headings != expected:
        missing = [title for title in expected if title not in actual.headings]
        raise ValueError(f'Markdown 标题未正确渲染：{missing}')


def main():
    paths = sorted([*ROOT.glob('*.md'), *(ROOT / 'examples').rglob('*.md')])
    for path in paths:
        try:
            check_document(path.read_text())
        except ValueError as error:
            raise ValueError(f'{path.relative_to(ROOT)}：{error}') from error
    print(f'通过：{len(paths)} 份 Markdown 的全部标题均正确渲染为 HTML 标题')


if __name__ == '__main__':
    main()
