# 配置选项

所有选项都是 tmux 窗口选项，前缀为 `@tmux_window_name_`。

> **注意**：选项使用 Python `eval()` 解析，请注意用户输入安全。

## Shell 程序

Shell 程序会显示目录名而非程序名。

```tmux.conf
set -g @tmux_window_name_shells "['bash', 'fish', 'sh', 'zsh']"
```

## 目录程序

同时显示目录名的程序。

示例：`git diff` 在 `~/my_repo` → `git diff:my_repo`

```tmux.conf
set -g @tmux_window_name_dir_programs "['nvim', 'vim', 'vi', 'git']"
```

## 忽略程序

检测活跃程序时跳过。

```tmux.conf
set -g @tmux_window_name_ignored_programs "['sqlite3']"
```

## 最大名称长度

```tmux.conf
set -g @tmux_window_name_max_name_len "20"
```

## 使用波浪号

用 `~` 替换 `$HOME`。

```tmux.conf
set -g @tmux_window_name_use_tilde "True"
```

## 显示程序参数

```tmux.conf
set -g @tmux_window_name_show_program_args "True"
```

## 替换规则

用正则替换程序命令行。

```tmux.conf
# 替换 ipython 路径
set -g @tmux_window_name_substitute_sets "[('.+ipython([32])', 'ipython\g<1>')]"
```

默认包含：
- `ipython2/3` → `ipython2/3`
- `/usr/bin/...` → `...`
- `bash /path/script` → `script`
- `poetry shell` → `poetry`

调试命令：

```bash
python3 -m tmux_window_name.cli --print_programs
```

## 目录替换规则

用正则替换目录名。

```tmux.conf
set -g @tmux_window_name_dir_substitute_sets "[('tmux-(.+)', '\g<1>')]"
```

## 图标样式

| 样式 | 结果 |
|------|------|
| `name` | `nvim` |
| `icon` | `` |
| `name_and_icon` | ` nvim` |
| `dir_and_icon` | ``（带目录） |

```tmux.conf
set -g @tmux_window_name_icon_style "'name_and_icon'"
```

## 自定义图标

```tmux.conf
set -g @tmux_window_name_custom_icons '{"python": "🐍", "go": ""}'
```

内置图标包括 nvim、vim、git、python、node、docker、go、rust 等。

## 忽略程序差异

无论程序是否相同，始终区分路径。

```tmux.conf
set -g @tmux_window_name_ignore_program_diffs "True"
```

使用场景：不启用时，`~/projects/app` 的 shell 显示 `app`（当其他窗口运行 vim），vim 退出后变为 `projects/app`。启用后名称保持稳定。

## 日志级别

```tmux.conf
set -g @tmux_window_name_log_level "'DEBUG'"
```

日志输出到 `/tmp/tmux-window-name.log`。