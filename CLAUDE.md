# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A tmux plugin that names windows smartly by showing the shortest non-conflicting directory path and detecting running programs.

## Commands

```bash
# Run tests
pytest

# Format code (required before PR)
ruff format

# Debug: print programs in current session
./scripts/rename_session_windows.py --print_programs
```

## Architecture

**Entry Point**: `tmux_window_name.tmux` (bash) sets up tmux hooks and checks libtmux dependency.

**Core Script**: `scripts/rename_session_windows.py`
- Uses libtmux to interact with tmux server
- Gets active panes via `ps -a -oppid,command` to detect running programs
- Renames windows based on program name + exclusive directory path

**Path Logic**: `scripts/path_utils.py`
- `get_exclusive_paths()` - finds shortest non-conflicting directory display names across all panes
- `get_uncommon_path()` - compares two paths to find their diverging parts

**Configuration**: All options are tmux options prefixed with `@tmux_window_name_` (e.g., `@tmux_window_name_shells`, `@tmux_window_name_dir_programs`). Options are read via `get_option()` and evaluated with `eval()`.

**Hook System**: Uses tmux hooks `after-select-window` and `after-new-window` to trigger renaming. Preserves user-renamed windows via `@tmux_window_name_enabled` flag.