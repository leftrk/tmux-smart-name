# tmux-smart-name

[English](README.md) | [中文](README_CN.md)

Smart tmux window names like IDE tablines.

![Screenshot](screenshots/example.png)

## Quick Example

Windows with same directory basename get disambiguated:

| Path | Display |
|------|---------|
| `~/projects/app` | `projects/app` |
| `~/work/app` | `work/app` |
| `~/projects/app` (nvim) | `nvim:projects/app` |

See [tests](tests/) for more scenarios.

## Installation

> **Recommended**: Use with [Oh My Tmux](https://github.com/gpakosz/.tmux) for best experience.

### Homebrew (recommended)

```bash
brew install leftrk/tap/tmux-smart-name
```

Add to `~/.tmux.conf`:

```tmux.conf
run-shell $(brew --prefix tmux-smart-name)/libexec/tmux_window_name.tmux
```

### TPM

```tmux.conf
set -g @plugin 'leftrk/tmux-smart-name'
```

Press `prefix + I` to install.

## Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `@tmux_window_name_max_name_len` | Max window name length | `20` |
| `@tmux_window_name_use_tilde` | Replace `$HOME` with `~` | `False` |
| `@tmux_window_name_icon_style` | Icon display style | `'name'` |

Example:

```tmux.conf
set -g @tmux_window_name_max_name_len "30"
set -g @tmux_window_name_icon_style "'name_and_icon'"
```

See [docs/options.md](docs/options.md) for all configuration options.

## Hooks

Automatic rename after nvim launch/exit or directory change.

See [docs/hooks.md](docs/hooks.md) for examples.

## Notes

- Load before `tmux-resurrect` if using it
- `tmux rename-window ""` re-enables auto-rename after manual rename

## Development

```bash
uv sync --group dev
uv run pytest
uv run ruff format
```

## License

[MIT](LICENSE)