---
name: myskills
description: Update the custom skills and their MCP setup from warner-benjamin/skills. Use when the user asks to refresh or reinstall these personal skills.
---

# My Skills

Update the custom skills from `https://github.com/warner-benjamin/skills.git`:

- Pull or clone the repository and its submodules recursively.
- Run `python3 <checkout>/myskills/scripts/install.py` from the updated checkout. It installs top-level skills, follows skill symlinks, and replaces installed versions without backups. Nested reference skills are not installed separately.
- The script also registers quiet-polling and reloads MCP connections. It preserves custom settings and checks tool discovery without scheduling a wake. It requires Python 3.11+ and Codex on `PATH` (`codex.exe` on Windows).
- Installation uses `$CODEX_HOME` or `~/.codex`. Use `--codex-home PATH` to choose another installation.

To register or reload quiet-polling without reinstalling skills, run `python3 <installed-skills>/quiet-polling/scripts/setup_mcp.py`. Setup details are in quiet-polling's `docs/maintenance.md`.
