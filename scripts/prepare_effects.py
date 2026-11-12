#!/usr/bin/env python3
"""贡献效果产物：校验第三方 SVG，并清理生成器附带的行尾空白。"""

from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
from effect_assets import effect_sources

SOURCES = effect_sources()


def main():
    """所有输入通过校验后，再写入明确的公开产物路径。"""
    outputs = {}
    for source, name in SOURCES.items():
        text = (ROOT / source).read_text()
        normalized = '\n'.join(line.rstrip() for line in text.splitlines()).rstrip() + '\n'
        root = ET.fromstring(normalized)
        if root.tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError(f'{source} 不是有效 SVG')
        if any(element.tag.rsplit('}', 1)[-1] == 'script' for element in root.iter()):
            raise ValueError(f'{source} 含脚本节点')
        outputs[name] = normalized
    target = ROOT / 'static/effects'
    target.mkdir(parents=True, exist_ok=True)
    for name, text in outputs.items():
        (target / name).write_text(text)
    print(f'{len(outputs)} 份贡献效果已校验并规范化')


if __name__ == '__main__':
    main()
