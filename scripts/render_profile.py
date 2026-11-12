#!/usr/bin/env python3
"""个人主页：统一生成双语介绍与效果画廊，并检查 Markdown 和本地资源。"""

import argparse
import re
import shlex
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = "其他一些好看的效果.md"
STATS = "https://github-stats-extended.vercel.app"
ROAST = "https://ghfind.com/api/card/mini/haers?variant=radar&theme=dark&lang=zh"
PROJECTS = [
    ("zhao-resource", "小赵资源站", "https://kuake.netlify.app/"),
    ("xieke-releases", "歇刻", "https://github.com/haers/xieke-releases/releases"),
    ("zhao-book-public", "小赵书库", "https://github.com/haers/zhao-book-public"),
]


def picture(light, dark, alt, width=440):
    """按 GitHub 支持的 picture 语法切换主题。"""
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{dark}" />
  <img src="{light}" alt="{alt}" width="{width}" align="top" />
</picture>'''


def stats_card(kind="stats", english=False):
    """开发统计：使用同一配色生成双语替代文本。"""
    path = "/api?username=haers&show_icons=true" if kind == "stats" else "/api/top-langs/?username=haers&layout=compact"
    url = STATS + path + "&hide_border=true&disable_animations=true"
    alt = "Public GitHub development statistics for haers" if kind == "stats" else "Languages used in haers public repositories"
    if not english:
        alt = "haers 的公开 GitHub 开发统计" if kind == "stats" else "haers 的公开仓库语言分布"
    return picture(url + "&theme=default&title_color=0969da&icon_color=0969da", url + "&theme=github_dark&title_color=58a6ff&icon_color=58a6ff", alt, 400)


def skills(english=False):
    """技术图标：每行六个，沿用仓库内的本地 SVG。"""
    alt = "Java, Spring, MySQL, Redis, Python, Vue, Nuxt, TypeScript, Tailwind CSS, Git, Docker, Linux"
    return f'<img src="static/svg/skillWap.svg" alt="{alt}" width="340" />'


def snake(english=False):
    """贡献动画：按系统主题选择仓库内的 SVG。"""
    alt = "Animated snake following haers GitHub contribution grid" if english else "haers 的 GitHub 贡献贪吃蛇动画"
    return picture("github-contribution-snake/github-contribution-grid-snake.svg", "github-contribution-snake/github-contribution-grid-snake-dark.svg", alt, 850)


def roast():
    """评分卡：保留用户指定的 ghfind 动态链接。"""
    return f"[![GitHub Roast 评分卡]({ROAST})](https://ghfind.com/u/haers?ref=badge)"


def pin(repo="zhao-resource", name="小赵资源站", english=False):
    """项目卡片：使用原生描述行数参数统一高度，容器提供组间距。"""
    base = f"{STATS}/api/pin/?username=haers&repo={repo}&description_lines_count=3&hide_border=true"
    light = base + "&theme=default&title_color=0969da&icon_color=0969da"
    dark = base + "&theme=github_dark&title_color=58a6ff&icon_color=58a6ff"
    alt = f"{repo} repository card" if english else f"{name}仓库卡片"
    card = picture(light, dark, alt, 390).replace("\n", "")
    return f'<a href="https://github.com/haers/{repo}">{card}</a>'


def pair(left, right):
    """双图独立成段，宽屏并排、窄屏自然换行，保留图卡内边距。"""
    return '<p>\n' + left + '\n' + right + '\n</p>'


def project_cards(english=False):
    """两张主卡成组，其他项目由文字入口与 GitHub 置顶区承载。"""
    return pair(*(pin(repo, name, english) for repo, name, _ in PROJECTS[:2]))


def code_block(snippet, language=None):
    """样例代码直接展开，内容与上方预览一致。"""
    if language is None:
        language = "html" if snippet.lstrip().startswith("<") else "markdown"
    return f"```{language}\n{snippet}\n```"


def profile(english=False):
    """恢复介绍、技能、作品、统计、贡献与联系的原版分块。"""
    if english:
        title = "👋 Hi, I’m Xiao Zhao!"
        intro = "I’m a backend developer working mainly with Java. I also enjoy building frontend projects, desktop tools, and automation.\n\nHere I share things I build, notes from learning, and a little of my curiosity about software."
        nav = f"[中文](README.md) · **English** · [README examples]({GALLERY})"
        skill_title, project_title, stats_title = "🚀 Skills", "💻 Projects", "📊 GitHub stats"
        skill_text = "- **Backend** · Java / Spring Boot / MySQL / Redis / Python\n- **Frontend** · Vue / Nuxt / TypeScript / Tailwind CSS\n- **Tools** · Git / Docker / Linux"
        activity_title, contact_title = "🐍 Contributions", "📫 Get in touch"
        contact = "Questions, feedback, or ideas? [Open an issue](https://github.com/haers/haers/issues)."
        entries = "[Resource directory](https://kuake.netlify.app/) · [Download Xieke](https://github.com/haers/xieke-releases/releases) · [Book library](https://github.com/haers/zhao-book-public)"
    else:
        title = "👋 你好，我是小赵！"
        intro = "我是一名以 Java 为主的后端开发者，也喜欢折腾前端、桌面工具和自动化。\n\n在这里分享自己的项目、学习笔记和一些有趣的想法，平时也喜欢拿手机拍拍照。"
        nav = f"**中文** · [English](README-en.md) · [效果样例]({GALLERY})"
        skill_title, project_title, stats_title = "🚀 我的技能", "💻 我的项目", "📊 GitHub 数据"
        skill_text = "- **后端开发** · Java / Spring Boot / MySQL / Redis / Python\n- **前端开发** · Vue / Nuxt / TypeScript / Tailwind CSS\n- **工具与环境** · Git / Docker / Linux"
        activity_title, contact_title = "🐍 贡献记录", "📫 联系与交流"
        contact = "如果你有项目问题、使用反馈，或者想交流一些有趣的想法，欢迎 [提一个 Issue](https://github.com/haers/haers/issues)。"
        entries = "[逛逛资源站](https://kuake.netlify.app/) · [下载歇刻](https://github.com/haers/xieke-releases/releases) · [小赵书库](https://github.com/haers/zhao-book-public)"
    return f'''<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->
# {title}

{intro}

{nav}

{roast()}

## {skill_title}

{skill_text}

{skills(english)}

## {project_title}

{project_cards(english)}

{entries}

## {stats_title}

{pair(stats_card(english=english), stats_card("languages", english))}

## {activity_title}

{snake(english)}

## {contact_title}

{contact}
'''


def effect_workflow(kind):
    """提供独立可运行的样例工作流，复制者无需安装本仓生成脚本。"""
    if kind == "3d":
        action = """      - uses: yoshi389111/github-profile-3d-contrib@7d95e7d4cdc028dd1e1cbd957d65f35efb12ae39
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          USERNAME: ${{ github.repository_owner }}"""
        sources = ["profile-3d-contrib/profile-green.svg", "profile-3d-contrib/profile-night-green.svg"]
        targets = ["static/effects/profile-green.svg", "static/effects/profile-night-green.svg"]
    else:
        action = """      - uses: abozanona/pacman-contribution-graph@70945878b1118303b37b88060fc7145e1a57d7b1
        with:
          github_user_name: ${{ github.repository_owner }}
          games: pacman"""
        sources = ["dist/pacman-contribution-graph.svg", "dist/pacman-contribution-graph-dark.svg"]
        targets = ["static/effects/pacman.svg", "static/effects/pacman-dark.svg"]
    copies = "\n".join(f"          cp {source} {target}" for source, target in zip(sources, targets))
    paths = " ".join(targets)
    return f'''name: generate-{kind}-contribution
on:
  workflow_dispatch:
  schedule:
    - cron: '15 0 * * *'
  push:
    branches: [main]
permissions:
  contents: write
concurrency:
  group: generate-{kind}
  cancel-in-progress: false
jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 12
    steps:
      - uses: actions/checkout@v5
{action}
      - name: Collect and publish
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p static/effects
{copies}
          python3 - <<'PYTHON'
          from pathlib import Path
          import xml.etree.ElementTree as ET
          for name in {targets!r}:
              path = Path(name)
              text = '\\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\\n'
              ET.fromstring(text)
              path.write_text(text)
          PYTHON
          git add -- {paths}
          if git diff --cached --quiet; then
            exit 0
          fi
          git diff --cached --check
          git config user.name 'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git commit -m 'chore: update contribution graph'
          git push --dry-run origin HEAD:main
          git push origin HEAD:main'''


def advanced_examples():
    """已生成的贡献效果使用真实产物，并附上可直接复制的工作流。"""
    sections = []
    examples = [
        ("3D 贡献日历", "static/effects/profile-green.svg", "static/effects/profile-night-green.svg"),
        ("吃豆人贡献动画", "static/effects/pacman.svg", "static/effects/pacman-dark.svg"),
    ]
    for index, (title, light, dark) in enumerate(examples):
        if (ROOT / light).is_file() and (ROOT / dark).is_file():
            preview = picture(light, dark, f"haers 的{title}", 850)
            content = f"## {title}\n\n{preview}\n\n{code_block(preview)}\n"
            content += "\n### GitHub Actions\n\n" + code_block(effect_workflow("3d" if index == 0 else "pacman"), "yaml") + "\n"
            sections.append(content)
    return sections


def gallery():
    """效果样例：标题、真实预览和完整代码直接展开。"""
    intro = "👋 你好，我是小赵！\n\nJava 后端开发 · 桌面工具与自动化 · 喜欢摄影"
    listed_intro = "\n".join([
        "- 👋 大家好，我是 haers",
        "- 💻 软件研发工程师，主要使用 Java",
        "- 🔧 喜欢折腾前端、桌面工具和自动化",
        "- 📷 喜欢手机摄影",
        "- 📫 [联系我](https://github.com/haers/haers/issues)",
    ])
    sections = [
        ("简短介绍", intro),
        ("列表介绍", listed_intro),
        ("评分雷达卡", roast()),
        ("技术图标", skills()),
        ("仓库卡片", project_cards()),
        ("开发统计", pair(stats_card(), stats_card("languages"))),
        ("贡献贪吃蛇", snake()),
    ]
    blocks = [f"## {title}\n\n{preview}\n\n{code_block(preview)}\n" for title, preview in sections]
    blocks.extend(advanced_examples())
    toc = " · ".join(f"[{title}](#{title})" for title, _ in sections)
    if len(blocks) > len(sections):
        toc += " · [3D 贡献日历](#3d-贡献日历) · [吃豆人贡献动画](#吃豆人贡献动画)"
    sources = "[Skill Icons](https://github.com/tandpfun/skill-icons) · [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended) · [snk](https://github.com/Platane/snk) · [ghfind](https://ghfind.com) · [3D Contrib](https://github.com/yoshi389111/github-profile-3d-contrib) · [Pac-Man](https://github.com/abozanona/pacman-contribution-graph)"
    return "<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->\n# GitHub 主页效果样例\n\n[返回主页](README.md) · [English](README-en.md)\n\n" + toc + "\n\n" + "\n".join(blocks) + "\n---\n\n" + sources + "\n"


def validate(path, text):
    """检查有效展示内容，避免生成失效的本地入口或缺少说明的图片。"""
    assert len(re.findall(r"^# ", text, re.M)) == 1, f"{path} 应只有一个一级标题"
    visible = re.sub(r"```.*?```", "", text, flags=re.S)
    assert "undefined" not in visible
    assert not re.search(r"\]\(\s*\)", visible)
    for tag in re.findall(r"<img\b[^>]*>", visible):
        assert re.search(r'alt="[^"]+"', tag), f"图片缺少内容说明：{path}"
    for link in re.findall(r"\]\(([^)]+)\)", visible) + re.findall(r'(?:src|srcset)="([^"]+)"', visible):
        if not link.startswith(("https://", "#")):
            assert (ROOT / link).is_file(), f"本地链接缺失：{path} / {link}"
    assert "<details" not in visible, f"{path} 的内容应直接展开"


def validate_workflow():
    """两个自动生成任务都只暂存明确的公开产物。"""
    scopes = {
        'snk.yml': {
            'github-contribution-snake/github-contribution-grid-snake.svg',
            'github-contribution-snake/github-contribution-grid-snake-dark.svg',
        },
        'effects.yml': {
            'static/effects/profile-green.svg',
            'static/effects/profile-night-green.svg',
            'static/effects/pacman.svg',
            'static/effects/pacman-dark.svg',
            GALLERY,
        },
    }
    for name, expected in scopes.items():
        workflow = (ROOT / '.github/workflows' / name).read_text()
        commands = [line.strip() for line in workflow.splitlines()]
        staging = [line for line in commands if line.startswith('git add ')]
        assert len(staging) == 1, name
        assert set(shlex.split(staging[0])[3:]) == expected, name
        assert 'ghaction-github-pages' not in workflow
        assert '--force' not in workflow
        assert 'git push --dry-run origin HEAD:main' in commands
        assert 'cancel-in-progress: false' in workflow
    for name in scopes['snk.yml']:
        root = ET.parse(ROOT / name).getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只检查生成文件是否最新")
    args = parser.parse_args()
    files = {"README.md": profile(), "README-en.md": profile(True), GALLERY: gallery()}
    for name, text in files.items():
        if args.check:
            if (ROOT / name).read_text() != text:
                sys.exit(f"{name} 已过期，请运行 python3 scripts/render_profile.py")
        else:
            (ROOT / name).write_text(text)
    for name, text in files.items():
        validate(name, text)
    for name in ("skillPc.svg", "skillWap.svg"):
        root = ET.parse(ROOT / "static/svg" / name).getroot()
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
    for path in (ROOT / 'static/effects').glob('*.svg'):
        root = ET.parse(path).getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg', str(path)
    validate_workflow()
    print("通过：三份 Markdown 同源生成、链接、图片说明、标题层级、SVG 与工作流暂存范围")


if __name__ == "__main__":
    main()
