# tmux-window-name

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

### Homebrew (recommended)

```bash
brew tap leftrk/tmux-window-name https://github.com/leftrk/tmux-window-name
brew install tmux-window-name
```

Add to `~/.tmux.conf`:

```tmux.conf
run-shell $(brew --prefix tmux-window-name)/libexec/tmux_window_name.tmux
```

### TPM

```tmux.conf
set -g @plugin 'leftrk/tmux-window-name'
```

Press `prefix + I` to install.

### Manual

```bash
git clone https://github.com/leftrk/tmux-window-name.git ~/path
```

```tmux.conf
run-shell ~/path/tmux_window_name.tmux
```

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