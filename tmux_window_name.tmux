#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Auto-install libtmux if not available
LIBTMUX_AVAILABLE=$(python3 -c "import importlib.util; print(importlib.util.find_spec('libtmux') is not None)" 2>/dev/null)
if [ "$LIBTMUX_AVAILABLE" != "True" ]; then
    tmux display "Installing libtmux dependency..."
    # Try uv first, fallback to pip if uv not available
    if command -v uv &> /dev/null; then
        uv pip install libtmux 2>/dev/null
    else
        python3 -m pip install --user libtmux 2>/dev/null
    fi
    # Verify installation
    LIBTMUX_AVAILABLE=$(python3 -c "import importlib.util; print(importlib.util.find_spec('libtmux') is not None)" 2>/dev/null)
    if [ "$LIBTMUX_AVAILABLE" != "True" ]; then
        tmux display "ERROR: tmux-window-name - Failed to install libtmux. Install uv (recommended) or run: python3 -m pip install --user libtmux"
        exit 0
    fi
    tmux display "libtmux installed successfully!"
fi

# Set PYTHONPATH to include the package directory for TPM/manual installs
export PYTHONPATH="$CURRENT_DIR:$PYTHONPATH"

tmux set -g automatic-rename on # Set automatic-rename on to make #{automatic-rename} be on when a new window is been open without a name
tmux set-hook -g 'after-new-window[8921]' 'set -wF @tmux_window_name_enabled \#\{automatic-rename\} ; set -w automatic-rename off'
tmux set-hook -g 'after-select-window[8921]' "run-shell -b \"PYTHONPATH='$CURRENT_DIR' python3 -m tmux_window_name.cli\""

############################################################################################
### Hacks for preserving users custom window names, read more at enable_user_rename_hook ###
############################################################################################

PYTHONPATH="$CURRENT_DIR" python3 -m tmux_window_name.cli --enable_rename_hook

# Disabling rename hooks when tmux-ressurect restores the sessions
tmux set -g @resurrect-hook-pre-restore-all "PYTHONPATH='$CURRENT_DIR' python3 -m tmux_window_name.cli --disable_rename_hook"
tmux set -g @resurrect-hook-post-restore-all "PYTHONPATH='$CURRENT_DIR' python3 -m tmux_window_name.cli --post_restore"