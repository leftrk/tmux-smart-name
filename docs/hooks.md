# Hooks

Automatic rename triggers beyond the default `after-select-window`.

## Neovim

Rename after nvim launches/exits:

```lua
local uv = vim.uv

vim.api.nvim_create_autocmd({ 'VimEnter', 'VimLeave' }, {
  callback = function()
    if vim.env.TMUX_PLUGIN_MANAGER_PATH then
      uv.spawn(vim.env.TMUX_PLUGIN_MANAGER_PATH .. '/tmux-window-name/tmux_window_name.tmux', {})
    elseif vim.env.TMUX then
      -- Homebrew/manual install
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

Rename after directory change:

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

# Use PROMPT_COMMAND or cd override
cd() {
  builtin cd "$@" && tmux-window-name
}
```

## tmux-resurrect Hooks

The plugin uses these hooks:

- `@resurrect-hook-pre-restore-all` - Disable rename during restore
- `@resurrect-hook-post-restore-all` - Re-enable after restore

Make sure `tmux-window-name` loads **before** `tmux-resurrect`.