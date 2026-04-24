# Hooks

除了默认的 `after-select-window`，还可以添加其他触发时机。

## Neovim

nvim 启动/退出时重命名：

```lua
local uv = vim.uv

vim.api.nvim_create_autocmd({ 'VimEnter', 'VimLeave' }, {
  callback = function()
    if vim.env.TMUX_PLUGIN_MANAGER_PATH then
      uv.spawn(vim.env.TMUX_PLUGIN_MANAGER_PATH .. '/tmux-window-name/tmux_window_name.tmux', {})
    elseif vim.env.TMUX then
      -- Homebrew/手动安装
      local path = vim.fn.system('brew --prefix tmux-window-name 2>/dev/null || echo ""')
      if path ~= '' then
        uv.spawn(path:gsub('\n', '') .. '/libexec/tmux_window_name.tmux', {})
      end
    end
  end,
})
```

## Vim Script

```vim
if !empty($TMUX) && has('job')
  autocmd VimEnter,VimLeave * call job_start(
    expand('$TMUX_PLUGIN_MANAGER_PATH/tmux-window-name/tmux_window_name.tmux')
  )
endif
```

## Shell (zsh)

切换目录后重命名：

```bash
tmux-window-name() {
  local script
  if [[ -n $TMUX_PLUGIN_MANAGER_PATH ]]; then
    script="$TMUX_PLUGIN_MANAGER_PATH/tmux-window-name/tmux_window_name.tmux"
  else
    script="$(brew --prefix tmux-window-name)/libexec/tmux_window_name.tmux"
  fi
  (python3 -m tmux_window_name.cli &)
}

add-zsh-hook chpwd tmux-window-name
```

## Shell (bash)

```bash
tmux-window-name() {
  (python3 -m tmux_window_name.cli &)
}

# 使用 PROMPT_COMMAND 或覆盖 cd
cd() {
  builtin cd "$@" && tmux-window-name
}
```

## tmux-resurrect Hooks

插件使用以下 hooks：

- `@resurrect-hook-pre-restore-all` - 恢复时禁用重命名
- `@resurrect-hook-post-restore-all` - 恢复后重新启用

确保 `tmux-window-name` 在 `tmux-resurrect` **之前**加载。