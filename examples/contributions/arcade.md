<!-- 由 scripts/render_profile.py 生成。 -->
# 街机贡献动画

[贡献动画](README.md) · [效果库](../README.md) · [个人主页](../../README.md)

示例账号 [haers](https://github.com/haers)。

## 吃豆人

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/haers/haers/main/static/effects/pacman-dark.svg" />
  <img src="https://raw.githubusercontent.com/haers/haers/main/static/effects/pacman.svg" alt="haers 的吃豆人贡献动画" width="850" align="top" />
</picture>

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/haers/haers/main/static/effects/pacman-dark.svg" />
  <img src="https://raw.githubusercontent.com/haers/haers/main/static/effects/pacman.svg" alt="haers 的吃豆人贡献动画" width="850" align="top" />
</picture>
```

### 工作流

```yaml
name: generate-pacman-pacman
on:
  workflow_dispatch:
  schedule:
    - cron: '15 0 * * *'
  push:
    branches: [main]
permissions:
  contents: write
concurrency:
  group: generate-pacman-pacman
  cancel-in-progress: false
jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 12
    steps:
      - uses: actions/checkout@v5
      - uses: abozanona/pacman-contribution-graph@70945878b1118303b37b88060fc7145e1a57d7b1
        with:
          github_user_name: ${{ github.repository_owner }}
          games: pacman
      - name: Collect and publish
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p static/effects
          cp dist/pacman-contribution-graph.svg static/effects/pacman.svg
          cp dist/pacman-contribution-graph-dark.svg static/effects/pacman-dark.svg
          python3 - <<'PYTHON'
          from pathlib import Path
          import xml.etree.ElementTree as ET
          for name in ['static/effects/pacman.svg', 'static/effects/pacman-dark.svg']:
              path = Path(name)
              text = '\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n'
              ET.fromstring(text)
              path.write_text(text)
          PYTHON
          git add -- static/effects/pacman.svg static/effects/pacman-dark.svg
          if git diff --cached --quiet; then
            exit 0
          fi
          git diff --cached --check
          git config user.name 'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git commit -m 'chore: update contribution graph'
          git push --dry-run origin HEAD:main
          git push origin HEAD:main
```

---

[Pac-Man Contribution Graph](https://github.com/abozanona/pacman-contribution-graph)
