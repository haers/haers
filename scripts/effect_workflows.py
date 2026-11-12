"""独立工作流示例：明确生成场景、发布路径与普通快进推送。"""

from effect_assets import CALENDAR_STYLES

def effect_workflow(kind, game="pacman", calendar="green"):
    """提供独立可运行的样例工作流，复制者无需安装本仓生成脚本。"""
    if kind == "3d":
        action = """      - uses: yoshi389111/github-profile-3d-contrib@7d95e7d4cdc028dd1e1cbd957d65f35efb12ae39
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          USERNAME: ${{ github.repository_owner }}"""
        sources = [f"profile-3d-contrib/profile-{style}.svg" for style in CALENDAR_STYLES]
        targets = [f"static/effects/profile-{style}.svg" for style in CALENDAR_STYLES]
    else:
        action = """      - uses: abozanona/pacman-contribution-graph@70945878b1118303b37b88060fc7145e1a57d7b1
        with:
          github_user_name: ${{ github.repository_owner }}
          games: pacman"""
        action = action.replace("games: pacman", f"games: {game}")
        sources = [f"dist/{game}-contribution-graph.svg", f"dist/{game}-contribution-graph-dark.svg"]
        targets = [f"static/effects/{game}.svg", f"static/effects/{game}-dark.svg"]
    copies = "\n".join(f"          cp {source} {target}" for source, target in zip(sources, targets))
    paths = " ".join(targets)
    return f'''name: generate-{kind}-{game if kind == "pacman" else calendar}
on:
  workflow_dispatch:
  schedule:
    - cron: '15 0 * * *'
  push:
    branches: [main]
permissions:
  contents: write
concurrency:
  group: generate-{kind}-{game if kind == "pacman" else calendar}
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

