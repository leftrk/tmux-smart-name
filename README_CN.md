# tmux-window-name

[English](README.md) | [中文](README_CN.md)

智能 tmux 窗口命名，类似 IDE 标签页。

智能 tmux 窗口命名，类似 IDE 标签页。

![截图](screenshots/example.png)

## 快速示例

相同目录名会自动区分：

| 路径 | 显示 |
|------|------|
| `~/projects/app` | `projects/app` |
| `~/work/app` | `work/app` |
| `~/projects/app` (nvim) | `nvim:projects/app` |

更多场景见 [测试文件](tests/)。

## 安装

### Homebrew（推荐）

```bash
brew install leftrk/tap/tmux-window-name
```

添加到 `~/.tmux.conf`：

```tmux.conf
run-shell $(brew --prefix tmux-window-name)/libexec/tmux_window_name.tmux
```

### TPM

```tmux.conf
set -g @plugin 'leftrk/tmux-window-name'
```

按 `prefix + I` 安装。

### 手动安装

```bash
git clone https://github.com/leftrk/tmux-window-name.git ~/path
```

```tmux.conf
run-shell ~/path/tmux_window_name.tmux
```

## 常用配置

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `@tmux_window_name_max_name_len` | 窗口名最大长度 | `20` |
| `@tmux_window_name_use_tilde` | 用 `~` 替换 `$HOME` | `False` |
| `@tmux_window_name_icon_style` | 图标显示样式 | `'name'` |

示例：

```tmux.conf
set -g @tmux_window_name_max_name_len "30"
set -g @tmux_window_name_icon_style "'name_and_icon'"
```

全部配置见 [docs/options_CN.md](docs/options_CN.md)。

## Hooks

nvim 启动/退出或切换目录后自动重命名。

示例见 [docs/hooks_CN.md](docs/hooks_CN.md)。

## 注意事项

- 使用 `tmux-resurrect` 时需在此插件之前加载
- 手动重命名后，`tmux rename-window ""` 可重新启用自动命名

## 开发

```bash
uv sync --group dev
uv run pytest
uv run ruff format
```

## 许可证

[MIT](LICENSE)