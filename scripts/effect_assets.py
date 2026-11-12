"""贡献效果目录：统一管理可选场景、生成器输入与公开产物路径。"""

ARCADE_GAMES = {
    'pacman': '吃豆人',
    'breakout': '打砖块',
    'galaga': '太空射击',
    'puzzle-bobble': '泡泡龙',
    'bomberman': '炸弹人',
    'minesweeper': '扫雷',
    'snake': '街机贪吃蛇',
    'tetris': '俄罗斯方块',
}
CALENDAR_STYLES = {
    'green': '绿色日历',
    'green-animate': '绿色动画',
    'season': '四季配色',
    'season-animate': '四季动画',
    'south-season': '南半球四季',
    'south-season-animate': '南半球四季动画',
    'night-view': '夜景',
    'night-green': '夜间绿色',
    'night-rainbow': '夜间彩虹',
    'gitblock': '积木',
}
DYNAMIC_PAGES = (
    'examples/contributions/arcade.md',
    'examples/contributions/3d-calendar.md',
)


def effect_sources():
    """所有文件逐项列出来源和目标，自动提交使用同一白名单。"""
    sources = {}
    for style in CALENDAR_STYLES:
        name = f'profile-{style}.svg'
        sources[f'profile-3d-contrib/{name}'] = name
    for game in ARCADE_GAMES:
        for suffix in ('', '-dark'):
            sources[f'dist/{game}-contribution-graph{suffix}.svg'] = f'{game}{suffix}.svg'
    return sources


def effect_paths():
    """返回完整的公开产物清单。"""
    return [f'static/effects/{name}' for name in effect_sources().values()]
