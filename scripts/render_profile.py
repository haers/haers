#!/usr/bin/env python3
"""统一生成双语主页与分类效果库，并检查文件、链接和自动发布范围。"""

import argparse
import re
import shlex
import sys
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET

from catalog_pages import catalog_pages
from effect_assets import DYNAMIC_PAGES, effect_paths
from profile_pages import ROOT, profile


def validate(name, text):
    """按当前文档位置解析相对链接，校验实际展示内容。"""
    visible = re.sub(r'```.*?```', '', text, flags=re.S)
    assert len(re.findall(r'^# ', visible, re.M)) == 1, f'{name} 应有一个一级标题'
    assert 'undefined' not in visible
    assert not re.search(r'\]\(\s*\)', visible)
    assert '<details' not in visible, f'{name} 的内容应直接展开'
    if name.startswith('examples/'):
        assert '```' not in text, f'{name} 预览页不应展示代码块'
    for tag in re.findall(r'<img\b[^>]*>', visible):
        assert re.search(r'alt="[^"]+"', tag), f'{name} 图片缺少说明'
    links = re.findall(r'\]\(([^)]+)\)', visible)
    links += re.findall(r'(?:src|srcset|href)="([^"]+)"', visible)
    for link in links:
        if link.startswith(('https://', '#')):
            continue
        path = unquote(link.split('#', 1)[0])
        assert (ROOT / Path(name).parent / path).is_file(), f'{name} 链接缺失：{link}'


def validate_workflows():
    """工作流只暂存明确产物，场景扩展时与产物清单同步。"""
    scopes = {
        'snk.yml': {
            'github-contribution-snake/github-contribution-grid-snake.svg',
            'github-contribution-snake/github-contribution-grid-snake-dark.svg',
        },
        'effects.yml': set(effect_paths()) | set(DYNAMIC_PAGES),
    }
    for name, expected in scopes.items():
        text = (ROOT / '.github/workflows' / name).read_text()
        lines = [line.strip() for line in text.splitlines()]
        commands = [line for line in lines if line.startswith('git add ')]
        assert len(commands) == 1, name
        assert set(shlex.split(commands[0])[3:]) == expected, name
        assert 'ghaction-github-pages' not in text and '--force' not in text
        assert 'git push --dry-run origin HEAD:main' in lines
        assert 'cancel-in-progress: false' in text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='只检查，不写文件')
    args = parser.parse_args()
    files = {'README.md': profile(), 'README-en.md': profile(True)}
    files.update(catalog_pages())
    for name, text in files.items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text() != text:
                sys.exit(f'{name} 已过期，请运行 python3 scripts/render_profile.py')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    for name, text in files.items():
        validate(name, text)
    for folder in ('static', 'github-contribution-snake'):
        for path in (ROOT / folder).rglob('*.svg'):
            assert ET.parse(path).getroot().tag == '{http://www.w3.org/2000/svg}svg', str(path)
    validate_workflows()
    assert not (ROOT / '其他一些好看的效果.md').exists(), '旧入口应迁入 examples/README.md'
    print(f'通过：{len(files)} 份同源 Markdown、相对链接、SVG 与工作流产物白名单')


if __name__ == '__main__':
    main()
