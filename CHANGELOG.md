# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Converted project to uv-managed Python package
- Switched to `uv_build` build backend
- Refactored `scripts/` into proper `tmux_window_name/` package
- Simplified README documentation (89 lines), detailed docs in `docs/`
- Added Chinese documentation (`README_CN.md`, `docs/options_CN.md`, `docs/hooks_CN.md`)
- Updated Homebrew Formula to use `pip_install(buildpath)`
- Auto-install libtmux dependency for TPM users (prefers uv over pip)
- Set Python requirement to `>=3.11` (matching libtmux dependency)

### Added
- GitHub Actions CI workflow (pytest + ruff)
- GitHub Actions release workflow (auto SHA256, Formula update)
- `.python-version` file (3.11)
- `pyproject.toml` with full project metadata

## [1.0.0] - 2024-XX-XX

### Added
- Smart window naming based on active programs
- Path disambiguation for same directory basenames
- Icon support with Nerd Font icons
- Custom icon configuration
- Multiple icon display styles (name, icon, name_and_icon, dir_and_icon)
- tmux-resurrect integration hooks
- Neovim/Vim/Shell hooks for automatic rename triggers

[Unreleased]: https://github.com/leftrk/tmux-window-name/compare/v1.0.0...dev
[1.0.0]: https://github.com/leftrk/tmux-window-name/releases/tag/v1.0.0