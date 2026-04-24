# Configuration Options

All options are tmux window options prefixed with `@tmux_window_name_`.

> **Note**: Options are evaluated with Python `eval()`. Be careful with user input.

## Shell Programs

Shell programs show directory instead of program name.

```tmux.conf
set -g @tmux_window_name_shells "['bash', 'fish', 'sh', 'zsh']"
```

## Directory Programs

Programs that show directory name alongside program.

Example: `git diff` in `~/my_repo` → `git diff:my_repo`

```tmux.conf
set -g @tmux_window_name_dir_programs "['nvim', 'vim', 'vi', 'git']"
```

## Ignored Programs

Programs to skip when detecting active program.

```tmux.conf
set -g @tmux_window_name_ignored_programs "['sqlite3']"
```

## Max Name Length

```tmux.conf
set -g @tmux_window_name_max_name_len "20"
```

## Use Tilde

Replace `$HOME` with `~` in window names.

```tmux.conf
set -g @tmux_window_name_use_tilde "True"
```

## Show Program Args

```tmux.conf
set -g @tmux_window_name_show_program_args "True"
```

## Substitute Sets

Replace program command lines using regex.

```tmux.conf
# Replace ipython paths
set -g @tmux_window_name_substitute_sets "[('.+ipython([32])', 'ipython\g<1>')]"
```

Default includes:
- `ipython2/3` → `ipython2/3`
- `/usr/bin/...` → `...`
- `bash /path/script` → `script`
- `poetry shell` → `poetry`

Debug with:

```bash
python3 -m tmux_window_name.cli --print_programs
```

## Directory Substitute Sets

Replace directory names using regex.

```tmux.conf
set -g @tmux_window_name_dir_substitute_sets "[('tmux-(.+)', '\g<1>')]"
```

## Icon Style

| Style | Result |
|-------|--------|
| `name` | `nvim` |
| `icon` | `` |
| `name_and_icon` | ` nvim` |
| `dir_and_icon` | `` (with dir) |

```tmux.conf
set -g @tmux_window_name_icon_style "'name_and_icon'"
```

## Custom Icons

```tmux.conf
set -g @tmux_window_name_custom_icons '{"python": "🐍", "go": ""}'
```

Built-in icons include nvim, vim, git, python, node, docker, go, rust, and more.

## Ignore Program Diffs

Always disambiguate paths regardless of program differences.

```tmux.conf
set -g @tmux_window_name_ignore_program_diffs "True"
```

Use case: Without this, `~/projects/app` (shell) shows `app` while vim runs in `~/work/app`, then changes to `projects/app` after vim exits. With `True`, names stay consistent.

## Log Level

```tmux.conf
set -g @tmux_window_name_log_level "'DEBUG'"
```

Logs go to `/tmp/tmux-window-name.log`.