"""效果库预览：总览与分类两层，打开分类即可浏览全部样式。"""

from urllib.parse import urlencode
import re

import profile_pages as ui
from effect_assets import ARCADE_GAMES, CALENDAR_STYLES

RAW = 'https://raw.githubusercontent.com/haers/haers/main/'
NAV = '[效果库](../README.md) · [个人主页](../../README.md)'


def public_assets(snippet):
    """源码采用完整资源地址，复制到其他 README 后仍能显示。"""
    def replace(match):
        attribute, path = match.groups()
        return f'{attribute}="{path if path.startswith("https://") else RAW + path}"'
    return re.sub(r'(src|srcset)="([^"]+)"', replace, snippet)


def section(title, preview):
    """具体场景只展示名称与实际效果。"""
    return f'### {title}\n\n{public_assets(preview)}\n'


def document(path, title, nav, body, source=None):
    """提供 GitHub 原生源码入口，预览页保持图文展示。"""
    code = f'https://github.com/haers/haers/blob/main/{path}?plain=1'
    result = f'<!-- 由 scripts/render_profile.py 生成。 -->\n# {title}\n\n{nav} · [查看源码]({code})\n\n{body.rstrip()}\n'
    if source:
        result += '\n---\n\n' + source + '\n'
    return result


def ghfind_image(variant='radar', theme='dark', lang='zh', large=False):
    """使用官方 OpenAPI 的尺寸、主题与语言参数。"""
    account = 'farion1231'
    path = f'/api/card/{account}' if large else f'/api/card/mini/{account}'
    params = {'variant': variant, 'theme': theme}
    if not large:
        params['lang'] = lang
    url = 'https://ghfind.com' + path + '?' + urlencode(params)
    return f'[![ghfind {variant} · 示例账号 {account}]({url})](https://ghfind.com/u/{account}?ref=badge)'


def badge_examples():
    """同页展示 ghfind 的卡片变体与 Shields 的徽章样式。"""
    parts = ['[ghfind](#ghfind) · [Shields](#shields)', '## ghfind', '示例账号 [farion1231](https://github.com/farion1231)。']
    badge = '[![ghfind 评分徽章 · farion1231](https://ghfind.com/api/badge/farion1231?lang=zh)](https://ghfind.com/u/farion1231?ref=badge)'
    parts.extend([
        section('20px 徽章', badge),
        section('中卡 · 六维条形', ghfind_image('bars', 'light')),
        section('中卡 · 雷达', ghfind_image()),
        section('窄条', ghfind_image('strip', 'auto')),
        section('大卡 · 1200 × 630', ghfind_image('score', 'dark', large=True)),
        section('自动主题', ghfind_image('bars', 'auto')),
        section('English', ghfind_image('bars', 'light', 'en')),
    ])
    base = 'https://ghfind.com/api/card/mini/farion1231?variant=radar&lang=zh'
    adaptive = '<a href="https://ghfind.com/u/farion1231?ref=badge">' + ui.picture(base + '&theme=light', base + '&theme=dark', 'farion1231 的 ghfind 双主题雷达卡') + '</a>'
    parts.append(section('跟随 GitHub 明暗主题', adaptive))
    parts.append('## Shields')
    for style in ('flat', 'flat-square', 'for-the-badge', 'social'):
        preview = f'[![Shields {style} 示例]({RAW}static/examples/shields-{style}.svg)](https://github.com/haers/haers)'
        parts.append(section(style, preview))
    parts.append(section('项目访问与下载入口', ui.project_entries()))
    return '\n\n'.join(parts)


def stats_image(kind='stats', layout='compact', dark=False):
    """使用公开账号展示不同统计布局。"""
    path = '/api' if kind == 'stats' else '/api/top-langs/'
    params = {'username': 'DenverCoder1', 'hide_border': 'true', 'disable_animations': 'true', 'theme': 'github_dark' if dark else 'default'}
    if kind == 'stats':
        params['show_icons'] = 'true'
    else:
        params['layout'], params['langs_count'] = layout, '8'
    url = ui.STATS + path + '?' + urlencode(params)
    return f'[![DenverCoder1 GitHub {kind}]({url})](https://github.com/DenverCoder1)'


def card_examples():
    """统计、语言和项目卡片在同一分类页面展示。"""
    parts = ['[开发统计](#开发统计) · [语言分布](#语言分布) · [项目卡片](#项目卡片)', '示例账号 [DenverCoder1](https://github.com/DenverCoder1)。', '## 开发统计', section('浅色', stats_image()), section('暗色', stats_image(dark=True)), '## 语言分布']
    for layout, title in [('compact', '紧凑'), ('normal', '列表'), ('donut', '环形'), ('pie', '饼图')]:
        parts.append(section(title, stats_image('languages', layout)))
    parts.append('## 项目卡片')
    for owner, repo, title in [('vuejs', 'core', 'Vue'), ('vitejs', 'vite', 'Vite')]:
        base = f'{ui.STATS}/api/pin/?username={owner}&repo={repo}&description_lines_count=3&hide_border=true'
        preview = f'<a href="https://github.com/{owner}/{repo}">' + ui.picture(base + '&theme=default', base + '&theme=github_dark', f'{owner}/{repo} 项目卡片', 400) + '</a>'
        parts.append(section(title, preview))
    return '\n\n'.join(parts)


def contribution_examples():
    """所有街机、3D 和贪吃蛇效果直接展示，工作流从页尾进入。"""
    parts = ['[街机动画](#街机动画) · [3D 日历](#3d-日历) · [贡献贪吃蛇](#贡献贪吃蛇)', '示例账号 [haers](https://github.com/haers)。', '## 街机动画']
    for game, title in ARCADE_GAMES.items():
        light, dark = f'static/effects/{game}.svg', f'static/effects/{game}-dark.svg'
        parts.append(section(title, ui.picture(light, dark, f'haers 的{title}贡献动画', 850)))
    parts.append('## 3D 日历')
    for style, title in CALENDAR_STYLES.items():
        parts.append(section(title, f'![haers 的{title}]({RAW}static/effects/profile-{style}.svg)'))
    parts.extend(['## 贡献贪吃蛇', section('明暗主题', ui.snake())])
    return '\n\n'.join(parts)


def catalog_pages():
    """总览直接链接四个完整分类页。"""
    intro = '👋 你好，我是小赵！\n\nJava 后端开发 · 桌面工具与自动化 · 喜欢摄影'
    profile = section('简短介绍', intro)
    profile += section('列表介绍', '- 👋 大家好，我是 haers\n- 💻 主要使用 Java\n- 📷 喜欢摄影\n- 📫 [联系我](https://github.com/haers/haers/issues)')
    profile += section('六列技能图标', ui.skills())
    profile += section('十二列技能图标', '<img src="static/svg/skillPc.svg" alt="技能图标 · 十二列" width="650" />')
    contributions = public_assets(ui.picture('static/effects/pacman.svg', 'static/effects/pacman-dark.svg', 'haers 的吃豆人贡献动画', 850))
    specs = [
        ('profile/README.md', '个人介绍与技能', intro, profile, '[Skill Icons](https://github.com/tandpfun/skill-icons)'),
        ('badges/README.md', '徽章与名片', ghfind_image(), badge_examples(), '[ghfind](https://ghfind.com/en/docs) · [Shields](https://shields.io) · [badge-maker](https://www.npmjs.com/package/badge-maker)'),
        ('cards/README.md', '统计与项目卡片', stats_image(), card_examples(), '[GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended)'),
        ('contributions/README.md', '贡献动画', contributions, contribution_examples(), '[街机动画](https://github.com/abozanona/pacman-contribution-graph) · [3D 日历](https://github.com/yoshi389111/github-profile-3d-contrib) · [snk](https://github.com/Platane/snk) · [街机与日历工作流](../../.github/workflows/effects.yml) · [贪吃蛇工作流](../../.github/workflows/snk.yml)'),
    ]
    pages, overview = {}, []
    for path, title, preview, body, source in specs:
        name = 'examples/' + path
        pages[name] = document(name, title, NAV, body, source)
        overview.append(f'## {title}\n\n{preview}\n\n[打开{title}]({path})\n')
    path = 'examples/README.md'
    pages[path] = document(path, 'GitHub 主页效果库', '[个人主页](../README.md) · [English](../README-en.md)', '\n'.join(overview))
    return pages
