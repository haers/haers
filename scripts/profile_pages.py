"""主页与共享片段：双语文案、图片主题与项目入口。"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = "examples/README.md"
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


def project_entries(english=False):
    """项目入口：使用本地 Shields 徽章说明访问、下载与仓库去向。"""
    language = 'en' if english else 'zh'
    labels = ('Browse resources', 'Download Xieke for macOS', 'View book repository') if english else ('资源站 · 在线浏览', '歇刻 · macOS 下载', '书库 · 查看仓库')
    entries = []
    for (_, _, url), name, label in zip(PROJECTS, ('resource', 'xieke', 'book'), labels):
        image = f'<img src="static/links/{name}-{language}.svg" alt="{label}" height="20" />'
        entries.append(f'<a href="{url}">{image}</a>')
    return '<p>\n' + '\n'.join(entries) + '\n</p>'


def profile(english=False):
    """恢复介绍、技能、作品、统计、贡献与联系的原版分块。"""
    if english:
        title = "👋 Hi, I’m Xiao Zhao!"
        intro = "I’m a backend developer working mainly with Java. I also enjoy building frontend projects, desktop tools, and automation.\n\nHere I share things I build, notes from learning, and a little of my curiosity about software."
        nav = f"[中文](README.md) · **English** · [Effect library]({GALLERY})"
        skill_title, project_title, stats_title = "🚀 Skills", "💻 Projects", "📊 GitHub stats"
        skill_text = "- **Backend** · Java / Spring Boot / MySQL / Redis / Python\n- **Frontend** · Vue / Nuxt / TypeScript / Tailwind CSS\n- **Tools** · Git / Docker / Linux"
        activity_title, contact_title = "👾 Contributions", "📫 Get in touch"
        contact = "Questions, feedback, or ideas? [Open an issue](https://github.com/haers/haers/issues)."
    else:
        title = "👋 你好，我是小赵！"
        intro = "我是一名以 Java 为主的后端开发者，也喜欢折腾前端、桌面工具和自动化。\n\n在这里分享自己的项目、学习笔记和一些有趣的想法，平时也喜欢拿手机拍拍照。"
        nav = f"**中文** · [English](README-en.md) · [效果库]({GALLERY})"
        skill_title, project_title, stats_title = "🚀 我的技能", "💻 我的项目", "📊 GitHub 数据"
        skill_text = "- **后端开发** · Java / Spring Boot / MySQL / Redis / Python\n- **前端开发** · Vue / Nuxt / TypeScript / Tailwind CSS\n- **工具与环境** · Git / Docker / Linux"
        activity_title, contact_title = "👾 贡献记录", "📫 联系与交流"
        contact = "如果你有项目问题、使用反馈，或者想交流一些有趣的想法，欢迎 [提一个 Issue](https://github.com/haers/haers/issues)。"
    return f'''<!-- 由 scripts/render_profile.py 生成，修改后运行生成器。 -->
# {title}

{intro}

{nav}

{project_entries(english)}

{roast()}

## {skill_title}

{skill_text}

{skills(english)}

## {project_title}

{project_cards(english)}

## {stats_title}

{pair(stats_card(english=english), stats_card("languages", english))}

## {activity_title}

{picture("static/effects/pacman.svg", "static/effects/pacman-dark.svg", "haers Pac-Man contribution animation" if english else "haers 的吃豆人贡献动画", 850)}

## {contact_title}

{contact}
'''

