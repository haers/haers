"""效果库：总览、分类入口和按来源展开的可复制示例。"""

from urllib.parse import urlencode
import re

import profile_pages as ui
from effect_assets import ARCADE_GAMES, CALENDAR_STYLES
from effect_workflows import effect_workflow

RAW = 'https://raw.githubusercontent.com/haers/haers/main/'
NAV = '[效果库](../README.md) · [个人主页](../../README.md)'


def public_assets(snippet):
    """公开样例使用完整资源地址，复制到其他 README 后仍能显示。"""
    def replace(match):
        attribute, path = match.groups()
        return f'{attribute}="{path if path.startswith("https://") else RAW + path}"'
    return re.sub(r'(src|srcset)="([^"]+)"', replace, snippet)


def section(title, preview, workflow=None):
    """每种场景直接展示效果、引用代码和可选工作流。"""
    preview = public_assets(preview)
    result = f'## {title}\n\n{preview}\n\n{ui.code_block(preview)}\n'
    if workflow:
        result += '\n### 工作流\n\n' + ui.code_block(workflow, 'yaml') + '\n'
    return result


def document(title, nav, body, source=None):
    """统一文档层级，来源与导航都使用真实链接。"""
    result = f'<!-- 由 scripts/render_profile.py 生成。 -->\n# {title}\n\n{nav}\n\n{body.rstrip()}\n'
    if source:
        result += '\n---\n\n' + source + '\n'
    return result


def ghfind_image(variant='radar', theme='dark', lang='zh', large=False):
    """使用官方 OpenAPI 支持的尺寸、主题与语言参数。"""
    account = 'farion1231'
    path = f'/api/card/{account}' if large else f'/api/card/mini/{account}'
    params = {'variant': variant, 'theme': theme}
    if not large:
        params['lang'] = lang
    url = 'https://ghfind.com' + path + '?' + urlencode(params)
    return f'[![ghfind {variant} · 示例账号 {account}]({url})](https://ghfind.com/u/{account}?ref=badge)'


def ghfind_page():
    """按卡片尺寸展开示例，公开账号明确归属。"""
    intro = '示例账号 [farion1231](https://github.com/farion1231)。\n\n'
    badge = '[![ghfind 评分徽章 · farion1231](https://ghfind.com/api/badge/farion1231?lang=zh)](https://ghfind.com/u/farion1231?ref=badge)'
    blocks = [
        section('20px 徽章', badge),
        section('中卡 · 六维条形', ghfind_image('bars', 'light')),
        section('中卡 · 雷达', ghfind_image()),
        section('窄条', ghfind_image('strip', 'auto')),
        section('大卡 · 1200 × 630', ghfind_image('score', 'dark', large=True)),
        section('自动主题', ghfind_image('bars', 'auto')),
        section('English', ghfind_image('bars', 'light', 'en')),
    ]
    base = 'https://ghfind.com/api/card/mini/farion1231?variant=radar&lang=zh'
    adaptive = '<a href="https://ghfind.com/u/farion1231?ref=badge">' + ui.picture(base + '&theme=light', base + '&theme=dark', 'farion1231 的 ghfind 双主题雷达卡') + '</a>'
    blocks.append(section('跟随 GitHub 明暗主题', adaptive))
    return document('ghfind 徽章与名片', '[徽章与名片](README.md) · ' + NAV, intro + '\n'.join(blocks), '[ghfind 官方说明](https://ghfind.com/en/docs) · [OpenAPI](https://ghfind.com/openapi.json)')


def shields_page():
    """Shields 样例用官方库生成的本地 SVG，提供稳定的公开引用。"""
    blocks = []
    for style in ('flat', 'flat-square', 'for-the-badge', 'social'):
        image = f'[![Shields {style} 示例]({RAW}static/examples/shields-{style}.svg)](https://github.com/haers/haers)'
        blocks.append(section(style, image))
    blocks.append(section('项目访问与下载入口', ui.project_entries()))
    return document('Shields 徽章', '[徽章与名片](README.md) · ' + NAV, '\n'.join(blocks), '[Shields](https://shields.io) · [badge-maker](https://www.npmjs.com/package/badge-maker)')


def stats_image(kind='stats', layout='compact', dark=False):
    """用贡献和语言分布丰富的公开账号演示统计卡。"""
    path = '/api' if kind == 'stats' else '/api/top-langs/'
    params = {'username': 'DenverCoder1', 'hide_border': 'true', 'disable_animations': 'true', 'theme': 'github_dark' if dark else 'default'}
    if kind == 'stats':
        params['show_icons'] = 'true'
    else:
        params['layout'] = layout
        params['langs_count'] = '8'
    url = ui.STATS + path + '?' + urlencode(params)
    return f'[![DenverCoder1 GitHub {kind}]({url})](https://github.com/DenverCoder1)'


def cards_pages():
    """统计和项目卡分别提供不同布局与主题。"""
    source = '[GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended)'
    stats = '示例账号 [DenverCoder1](https://github.com/DenverCoder1)。\n\n'
    stats += section('开发统计 · 浅色', stats_image())
    stats += section('开发统计 · 暗色', stats_image(dark=True))
    for layout, title in [('compact', '紧凑语言分布'), ('normal', '列表语言分布'), ('donut', '环形语言分布'), ('pie', '饼图语言分布')]:
        stats += section(title, stats_image('languages', layout))
    repos = []
    for owner, repo, title in [('vuejs', 'core', 'Vue'), ('vitejs', 'vite', 'Vite')]:
        base = f'{ui.STATS}/api/pin/?username={owner}&repo={repo}&description_lines_count=3&hide_border=true'
        image = f'<a href="https://github.com/{owner}/{repo}">' + ui.picture(base + '&theme=default', base + '&theme=github_dark', f'{owner}/{repo} 项目卡片', 400) + '</a>'
        repos.append(section(title, image))
    return {
        'examples/cards/github-stats.md': document('GitHub 开发与语言统计', '[统计与项目卡片](README.md) · ' + NAV, stats, source),
        'examples/cards/repositories.md': document('项目卡片', '[统计与项目卡片](README.md) · ' + NAV, '\n'.join(repos), source),
    }


def contribution_pages():
    """按游戏和配色展开真实贡献图，附独立工作流。"""
    games = []
    for game, title in ARCADE_GAMES.items():
        light, dark = f'static/effects/{game}.svg', f'static/effects/{game}-dark.svg'
        if (ui.ROOT / light).is_file() and (ui.ROOT / dark).is_file():
            games.append(section(title, ui.picture(light, dark, f'haers 的{title}贡献动画', 850), effect_workflow('pacman', game=game)))
    calendars = []
    for style, title in CALENDAR_STYLES.items():
        path = f'static/effects/profile-{style}.svg'
        if (ui.ROOT / path).is_file():
            image = f'![haers 的{title}]({RAW}{path})'
            calendars.append(section(title, image))
    calendars.append('## 工作流\n\n' + ui.code_block(effect_workflow('3d'), 'yaml'))
    return {
        'examples/contributions/arcade.md': document('街机贡献动画', '[贡献动画](README.md) · ' + NAV, '示例账号 [haers](https://github.com/haers)。\n\n' + '\n'.join(games), '[Pac-Man Contribution Graph](https://github.com/abozanona/pacman-contribution-graph)'),
        'examples/contributions/3d-calendar.md': document('3D 贡献日历', '[贡献动画](README.md) · ' + NAV, '示例账号 [haers](https://github.com/haers)。\n\n' + '\n'.join(calendars), '[GitHub Profile 3D Contrib](https://github.com/yoshi389111/github-profile-3d-contrib)'),
        'examples/contributions/snake.md': document('贡献贪吃蛇', '[贡献动画](README.md) · ' + NAV, section('明暗主题', ui.snake()), '[snk](https://github.com/Platane/snk) · [本仓生成工作流](../../.github/workflows/snk.yml)'),
    }


def catalog_pages():
    """总览每类一个代表预览，分类页再导航到完整场景。"""
    intro = '👋 你好，我是小赵！\n\nJava 后端开发 · 桌面工具与自动化 · 喜欢摄影'
    profile = section('简短介绍', intro)
    profile += section('列表介绍', '- 👋 大家好，我是 haers\n- 💻 主要使用 Java\n- 📷 喜欢摄影\n- 📫 [联系我](https://github.com/haers/haers/issues)')
    profile += section('六列技能图标', ui.skills())
    profile += section('十二列技能图标', '<img src="static/svg/skillPc.svg" alt="技能图标 · 十二列" width="650" />')
    badges = ghfind_image()
    contributions = public_assets(ui.picture('static/effects/pacman.svg', 'static/effects/pacman-dark.svg', 'haers 的吃豆人贡献动画', 850))
    pages = {
        'examples/profile/README.md': document('个人介绍与技能图标', NAV, profile, '[Skill Icons](https://github.com/tandpfun/skill-icons)'),
        'examples/badges/ghfind.md': ghfind_page(),
        'examples/badges/shields.md': shields_page(),
        'examples/badges/README.md': document('徽章与名片', NAV, f'## ghfind\n\n{badges}\n\n[尺寸、主题与语言场景](ghfind.md)\n\n## Shields\n\n![项目徽章]({RAW}static/links/resource-zh.svg)\n\n[样式与项目入口](shields.md)'),
        'examples/cards/README.md': document('统计与项目卡片', NAV, f'## GitHub 统计\n\n{stats_image()}\n\n[开发数据与语言布局](github-stats.md)\n\n[Vue / Vite 项目卡片](repositories.md)'),
        'examples/contributions/README.md': document('贡献动画', NAV, f'{contributions}\n\n| 场景 | 内容 |\n| --- | --- |\n| [街机动画](arcade.md) | 吃豆人、打砖块、太空射击、泡泡龙、炸弹人、扫雷、贪吃蛇、俄罗斯方块 |\n| [3D 日历](3d-calendar.md) | 绿色、四季、夜景、彩虹、积木等配色 |\n| [贡献贪吃蛇](snake.md) | 明暗主题 |'),
    }
    root = [
        ('个人介绍与技能', 'profile/README.md', intro),
        ('徽章与名片', 'badges/README.md', badges),
        ('统计与项目卡片', 'cards/README.md', stats_image()),
        ('贡献动画', 'contributions/README.md', contributions),
    ]
    body = []
    for title, path, preview in root:
        body.append(f'## {title}\n\n{preview}\n\n[查看全部场景]({path})\n')
    pages['examples/README.md'] = document('GitHub 主页效果库', '[个人主页](../README.md) · [English](../README-en.md)', '\n'.join(body))
    pages.update(cards_pages())
    pages.update(contribution_pages())
    return pages
