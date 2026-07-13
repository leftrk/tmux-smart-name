# Hooks

Automatic rename triggers beyond the default `after-select-window`.

## Neovim

Rename after nvim launches/exits:

```lua
local uv = vim.uv

vim.api.nvim_create_autocmd({ 'VimEnter', 'VimLeave' }, {
  callback = function()
    if vim.env.TMUX_PLUGIN_MANAGER_PATH then
      uv.spawn(vim.env.TMUX_PLUGIN_MANAGER_PATH .. '/tmux-smart-name/tmux_window_name.tmux', {})
    end
  end,
})
```

## Vim Script

```vim
if !empty($TMUX) && has('job')
  autocmd VimEnter,VimLeave * call job_start(
    expand('$TMUX_PLUGIN_MANAGER_PATH/tmux-smart-name/tmux_window_name.tmux')
  )
endif
```

## Shell (zsh)

Rename after directory change:

```bash
tmux-smart-name() {
  (python3 -m tmux_window_name.cli &)
}

add-zsh-hook chpwd tmux-smart-name
```

## Shell (bash)

```bash
tmux-smart-name() {
  (python3 -m tmux_window_name.cli &)
}

# Use PROMPT_COMMAND or cd override
cd() {
  builtin cd "$@" && tmux-smart-name
}
```

## tmux-resurrect Hooks

The plugin uses these hooks:

- `@resurrect-hook-pre-restore-all` - Disable rename during restore
- `@resurrect-hook-post-restore-all` - Re-enable after restore

Make sure `tmux-smart-name` loads **before** `tmux-resurrect`.