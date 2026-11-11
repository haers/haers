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
    url = STATS + path + "&hide_border=true"
    alt = "Public GitHub development statistics for haers" if kind == "stats" else "Languages used in haers public repositories"
    if not english:
        alt = "haers 的公开 GitHub 开发统计" if kind == "stats" else "haers 的公开仓库语言分布"
    return picture(url + "&theme=default&title_color=0969da&icon_color=0969da", url + "&theme=github_dark&title_color=58a6ff&icon_color=58a6ff", alt, 400)


def skills(english=False):
    """技术栈：桌面单行、窄屏双行共用本地图片。"""
    alt = "Frequently used technologies" if english else "常用技术"
    return f'''<picture>
  <source media="(max-width: 600px)" srcset="static/svg/skillWap.svg" />
  <img src="static/svg/skillPc.svg" alt="{alt} / Java, Spring, MySQL, Redis, Python, Vue, Nuxt, TypeScript, Tailwind CSS, Git, Docker, Linux" width="600" />
</picture>'''


def snake(english=False):
    """贡献动画：按系统主题选择仓库内的 SVG。"""
    alt = "Animated snake following haers GitHub contribution grid" if english else "haers 的 GitHub 贡献贪吃蛇动画"
    return picture("github-contribution-snake/github-contribution-grid-snake.svg", "github-contribution-snake/github-contribution-grid-snake-dark.svg", alt, 850)


def roast():
    """评分卡：保留用户指定的 ghfind 动态链接。"""
    return f"[![GitHub Roast 评分卡]({ROAST})](https://ghfind.com/u/haers?ref=badge)"


def pin(repo="zhao-resource", name="小赵资源站", english=False):
    """仓库卡片：桌面三列同高，手机切换为宽卡，均由第三方服务渲染。"""
    base = f"{STATS}/api/pin/?username=haers&repo={repo}&description_lines_count=3"
    light = "&theme=default&title_color=0969da&icon_color=0969da"
    dark = "&theme=github_dark&title_color=58a6ff&icon_color=58a6ff"
    alt = f"{repo} repository card" if english else f"{name}仓库卡片"
    return f'''<a href="https://github.com/haers/{repo}">
<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="{base}&card_width=400{dark}" />
  <source media="(max-width: 600px)" srcset="{base}&card_width=400{light}" />
  <source media="(prefers-color-scheme: dark)" srcset="{base}&card_width=260{dark}" />
  <img src="{base}&card_width=260{light}" alt="{alt}" />
</picture>
</a>'''


def project_cards(english=False):
    """统一项目区间隔，图片按容器宽度自然换行。"""
    return "&nbsp;&nbsp;\n".join(pin(repo, name, english) for repo, name, _ in PROJECTS)


def code_block(snippet):
    """折叠示例：为画廊中的实际预览提供可复制源码。"""
    language = "html" if snippet.lstrip().startswith("<") else "markdown"
    return f"<details>\n<summary>复制代码</summary>\n\n```{language}\n{snippet}\n```\n\n</details>"


def profile(english=False):
    """双语主页：用仓库卡片、技能图标和统计图构成主要内容。"""
    if english:
        title = "Hi, I’m Xiao Zhao / haers"
        intro = "Java backend developer · Desktop tools & automation · Photography"
        nav = f"[中文](README.md) · **English** · [Examples]({GALLERY})"
        project_title, stack_title, activity_title = "Projects", "Tech stack", "GitHub"
        footer = "[Get in touch](https://github.com/haers/haers/issues)"
        entries = " · ".join(f"[{repo}]({url})" for repo, _, url in PROJECTS)
        animation_title = "Contribution snake"
    else:
        title = "你好，我是小赵 / haers"
        intro = "Java 后端开发 · 桌面工具与自动化 · 喜欢摄影"
        nav = f"**中文** · [English](README-en.md) · [效果样例]({GALLERY})"
        project_title, stack_title, activity_title = "我的作品", "常用技术", "GitHub"
        footer = "[交流与反馈](https://github.com/haers/haers/issues)"
        entries = " · ".join(f"[{name}]({url})" for _, name, url in PROJECTS)
        animation_title = "贡献贪吃蛇"
    cards = project_cards(english)
    return f'''<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->
# {title}

{intro}

{nav}

## {project_title}

{cards}

{entries}

## {stack_title}

{skills(english)}

## {activity_title}

{stats_card(english=english)}
{stats_card("languages", english)}

{roast()}

<details>
<summary>{animation_title}</summary>

{snake(english)}

</details>

{footer}
'''


def gallery():
    """样例集：实际预览与对应代码成对展示。"""
    intro = "你好，我是小赵 / haers\n\nJava 后端开发 · 桌面工具与自动化 · 喜欢摄影"
    detailed_intro = "\n".join([
        "- 👋 大家好，我是 haers",
        "- 💻 软件研发工程师，主要使用 Java",
        "- 🛠 喜欢折腾前端、桌面工具和自动化",
        "- 📷 喜欢手机摄影",
        "- 📫 [联系我](https://github.com/haers/haers/issues)",
    ])
    sections = [
        ("简短介绍", intro),
        ("列表介绍", detailed_intro),
        ("技术图标", skills()),
        ("仓库卡片", project_cards()),
        ("开发统计", stats_card() + "\n" + stats_card("languages")),
        ("贡献贪吃蛇", snake()),
        ("评分雷达卡", roast()),
    ]
    blocks = [f"## {title}\n\n{preview}\n\n{code_block(preview)}\n" for title, preview in sections]
    sources = "[Skill Icons](https://github.com/tandpfun/skill-icons) · [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended) · [snk](https://github.com/Platane/snk) · [ghfind](https://ghfind.com)"
    return "<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->\n# GitHub 主页样例\n\n[返回主页](README.md) · [English](README-en.md)\n\n" + "\n".join(blocks) + "\n---\n\n" + sources + "\n"


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
    assert visible.count("<details>") == visible.count("</details>")


def validate_workflow():
    """限制自动生成任务的暂存范围，防止整目录发布覆盖主页内容。"""
    workflow = (ROOT / ".github/workflows/snk.yml").read_text()
    expected = {
        "github-contribution-snake/github-contribution-grid-snake.svg",
        "github-contribution-snake/github-contribution-grid-snake-dark.svg",
    }
    commands = [line.strip() for line in workflow.splitlines()]
    staging = [line for line in commands if line.startswith("git add ")]
    assert len(staging) == 1
    assert set(shlex.split(staging[0])[3:]) == expected
    assert "ghaction-github-pages" not in workflow
    assert "--force" not in workflow
    assert "git push --dry-run origin HEAD:main" in commands
    assert "cancel-in-progress: false" in workflow
    for path in expected:
        root = ET.parse(ROOT / path).getroot()
        assert root.tag == "{http://www.w3.org/2000/svg}svg"


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
    validate_workflow()
    print("通过：三份 Markdown 同源生成、链接、图片说明、标题层级、SVG 与工作流暂存范围")


if __name__ == "__main__":
    main()
