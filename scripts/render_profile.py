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
    ("zhao-resource", "小赵资源站", "学习与资源导航，按内容分类查找。", "A directory for learning materials and useful resources.", "JavaScript", "https://kuake.netlify.app/"),
    ("xieke-releases", "歇刻", "macOS 桌面休息提醒工具的安装包与更新入口。", "Downloads and updates for my macOS break reminder.", ("macOS · 发布与更新", "macOS · Releases"), "https://github.com/haers/xieke-releases/releases"),
    ("zhao-book-public", "小赵书库", "书库项目的公开静态成品。", "The published static edition of my book library.", ("静态站点", "Static site"), "https://github.com/haers/zhao-book-public"),
]


def picture(light, dark, alt, width=440):
    """按 GitHub 支持的 picture 语法切换主题。"""
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{dark}" />
  <img src="{light}" alt="{alt}" width="{width}" />
</picture>'''


def stats_card(kind="stats", english=False):
    """开发统计：使用同一配色生成双语替代文本。"""
    path = "/api?username=haers&show_icons=true" if kind == "stats" else "/api/top-langs/?username=haers&layout=compact"
    url = STATS + path + "&hide_border=true&title_color=58a6ff&icon_color=58a6ff"
    alt = "Public GitHub development statistics for haers" if kind == "stats" else "Languages used in haers public repositories"
    if not english:
        alt = "haers 的公开 GitHub 开发统计" if kind == "stats" else "haers 的公开仓库语言分布"
    return picture(url + "&theme=default", url + "&theme=github_dark", alt, 400)


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


def pin():
    """项目卡片：展示已核实的公开资源站仓库。"""
    base = STATS + "/api/pin/?username=haers&repo=zhao-resource&hide_border=true&title_color=58a6ff&icon_color=58a6ff"
    return '<a href="https://github.com/haers/zhao-resource">\n' + picture(base + "&theme=default", base + "&theme=github_dark", "小赵资源站仓库卡片") + '\n</a>'


def code_block(snippet):
    """折叠示例：为画廊中的实际预览提供可复制源码。"""
    return f"<details>\n<summary>展开查看代码</summary>\n\n```html\n{snippet}\n```\n\n</details>"


def profile(english=False):
    """双语页面共用结构与项目来源，正文按语言输出。"""
    if english:
        title = "Hi, I’m Xiao Zhao / haers"
        intro = "I build backend services with Java and explore frontend development, desktop tools, and automation.\n\nBased in China. I enjoy tinkering with software and taking photos."
        nav = f"[中文](README.md) · **English** · [Effect gallery]({GALLERY})"
        project_title, stack_title, activity_title = "Selected projects", "Tools I use", "Development activity"
        footer_title, footer = "Get in touch", "Have a question about a project or an idea to discuss? [Open an issue](https://github.com/haers/haers/issues)."
        tech = "**Backend** · Java / Spring Boot / MySQL / Redis / Python\n\n**Frontend** · Vue / Nuxt / TypeScript / Tailwind CSS\n\n**Tools** · Git / Docker / Linux"
        animation_title, score_title = "View contribution animation", "View ghfind score card"
        sources = "[Statistics source](https://github.com/stats-organization/github-stats-extended) · [Score details](https://ghfind.com/u/haers?ref=badge)"
    else:
        title = "你好，我是小赵 / haers"
        intro = "以 Java 后端开发为主，也折腾前端、桌面工具和自动化。\n\n在中国生活，喜欢探索软件，也喜欢随手拍照。"
        nav = f"**中文** · [English](README-en.md) · [效果画廊]({GALLERY})"
        project_title, stack_title, activity_title = "我的作品", "常用技术", "开发记录"
        footer_title, footer = "联系我", "项目问题、使用反馈或交流想法，欢迎 [提一个 Issue](https://github.com/haers/haers/issues)。"
        tech = "**后端** · Java / Spring Boot / MySQL / Redis / Python\n\n**前端** · Vue / Nuxt / TypeScript / Tailwind CSS\n\n**工具** · Git / Docker / Linux"
        animation_title, score_title = "展开贡献动画", "展开 ghfind 评分卡"
        sources = "[统计来源](https://github.com/stats-organization/github-stats-extended) · [查看评分详情](https://ghfind.com/u/haers?ref=badge)"
    projects = []
    for repo, name, zh, en, technology, entry in PROJECTS:
        label = repo if english else name
        link_label = "Explore" if english else "查看项目"
        technology = technology[int(english)] if isinstance(technology, tuple) else technology
        projects.append(f"### [{label}](https://github.com/haers/{repo})\n\n{en if english else zh}\n\n{technology} · [{link_label}]({entry})")
    # 单列卡片保留浏览顺序，图片由 GitHub 的宽度限制适配窄屏。
    return f'''<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->
# {title}

{nav}

{intro}

## {project_title}

{chr(10).join(p + chr(10) for p in projects)}
## {stack_title}

{tech}

{skills(english)}

## {activity_title}

{stats_card(english=english)}
{stats_card("languages", english)}

{sources}

<details>
<summary>{animation_title}</summary>

{snake(english)}

</details>

<details>
<summary>{score_title}</summary>

{roast()}

</details>

## {footer_title}

{footer}
'''


def gallery():
    """效果画廊：统一组织预览、源码与第三方来源。"""
    intro = "> 大家好，我是 haers，一名以 Java 开发为主的软件研发工程师。喜欢折腾工具，也喜欢手机摄影。"
    sections = [
        ("个人介绍", "用两句话说明开发方向与兴趣，适合放在主页开头。", intro, "Markdown 引用块", "https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax"),
        ("技术图标", "精选 12 个常用技术。窄屏切换为两行，图片与主页共用。", skills(), "Skill Icons", "https://github.com/tandpfun/skill-icons"),
        ("开发统计", "开发数据和语言分布跟随系统明暗主题。语言分布来自公开仓库，可点击来源了解统计口径。", stats_card() + "\n" + stats_card("languages"), "github-stats-extended", "https://github.com/stats-organization/github-stats-extended"),
        ("项目卡片", "用小赵资源站演示仓库卡片，点击卡片进入仓库。", pin(), "github-stats-extended", "https://github.com/stats-organization/github-stats-extended"),
        ("贡献动画", "贪吃蛇沿贡献格移动。主页默认折叠，按需展开。", '<details>\n<summary>展开贡献贪吃蛇</summary>\n\n' + snake() + '\n\n</details>', "Platane/snk", "https://github.com/Platane/snk"),
        ("评分雷达卡", "查看 ghfind 的等级与维度评分。第三方和 GitHub 图片缓存可能延迟，点击卡片查看当前评分详情。", roast(), "ghfind", "https://ghfind.com/en/docs"),
    ]
    blocks = []
    for title, description, preview, source, url in sections:
        blocks.append(f"## {title}\n\n{description}\n\n{preview}\n\n{code_block(preview)}\n\n来源 [{source}]({url})\n")
    return "<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->\n# GitHub 主页效果画廊\n\n[返回中文主页](README.md) · [English](README-en.md)\n\n先看效果，再展开代码。示例使用 haers 的公开资料，复制时替换用户名和仓库名。\n\n" + "\n".join(blocks)


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
