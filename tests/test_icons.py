#!/usr/bin/env python3

from dataclasses import dataclass
from unittest.mock import Mock

from tmux_window_name.cli import Options, IconStyle, get_program_icon, substitute_name, DEFAULT_PROGRAM_ICONS


@dataclass
class FakeServer:
    def __init__(self):
        self.cmd = Mock()
        self.cmd.return_value = self


def test_get_program_icon_built_in():
    """Test retrieving built-in program icons"""
    options = Options()
    assert get_program_icon('nvim', options) == DEFAULT_PROGRAM_ICONS['nvim']  # vim icon
    assert get_program_icon('python', options) == DEFAULT_PROGRAM_ICONS['python']  # python icon
    assert get_program_icon('nonexistent', options) == ''  # no icon


def test_get_program_icon_custom():
    """Test custom program icons override built-in ones"""
    options = Options(
        custom_icons={
            'custom_app': '󰀄',
            'nvim': '󰹻',  # override default vim icon
        }
    )
    assert get_program_icon('custom_app', options) == '󰀄'
    assert get_program_icon('nvim', options) == '󰹻'  # should use custom icon
    assert get_program_icon('python', options) == DEFAULT_PROGRAM_ICONS['python']  # should use built-in icon


def test_get_program_icon_with_path():
    """Test that program icons work with full paths"""
    options = Options()
    assert get_program_icon('/usr/bin/python', options) == DEFAULT_PROGRAM_ICONS['python']
    assert get_program_icon('/custom/path/nvim', options) == DEFAULT_PROGRAM_ICONS['nvim']


def test_get_program_icon_with_args():
    """Test that program icons work with command arguments"""
    options = Options()
    assert get_program_icon('python script.py --arg', options) == DEFAULT_PROGRAM_ICONS['python']
    assert get_program_icon('nvim file.txt', options) == DEFAULT_PROGRAM_ICONS['nvim']


def test_substitute_name_name_style():
    """Test window renaming with 'name' style (default)"""
    options = Options(icon_style=IconStyle.NAME)
    name, style = substitute_name('python', options.substitute_sets, options, True)
    assert name == 'python'
    assert not style.icon_set
    assert not style.only_icon


def test_substitute_name_icon_style():
    """Test window renaming with 'icon' style"""
    options = Options(icon_style=IconStyle.ICON)
    name, style = substitute_name('python', options.substitute_sets, options, True)
    assert name == DEFAULT_PROGRAM_ICONS['python']
    assert style.icon_set
    assert style.only_icon


def test_substitute_name_name_and_icon_style():
    """Test window renaming with 'name_and_icon' style"""
    options = Options(icon_style=IconStyle.NAME_AND_ICON)
    name, style = substitute_name('python', options.substitute_sets, options, True)
    assert name == f'{DEFAULT_PROGRAM_ICONS["python"]} python'
    assert style.icon_set
    assert not style.only_icon


def test_substitute_name_dir_and_icon_style():
    """Test window renaming with 'name_and_icon' style"""
    options = Options(icon_style=IconStyle.DIR_AND_ICON)
    name, style = substitute_name('python', options.substitute_sets, options, True)
    assert name == f'{DEFAULT_PROGRAM_ICONS["python"]}'
    assert style.icon_set
    assert not style.only_icon
    # Same behavior as NAME_AND_ICON for now


def test_substitute_name_custom_icon():
    """Test window renaming with custom icon"""
    options = Options(icon_style=IconStyle.NAME_AND_ICON, custom_icons={'python': '🐍'})
    name, style = substitute_name('python', options.substitute_sets, options, True)
    assert name == '🐍 python'
    assert style.icon_set
    assert not style.only_icon


def test_get_program_icon_with_colon():
    """Test that program icons work with program names containing colons"""
    options = Options()
    assert get_program_icon('python:3.9', options) == DEFAULT_PROGRAM_ICONS['python']
    assert get_program_icon('nvim:q', options) == DEFAULT_PROGRAM_ICONS['nvim']


def test_custom_icons_from_dictionary():
    """Test that custom icons can be parsed from a dictionary"""
    server = FakeServer()
    server.cmd.return_value.stdout = ['{"python": "🐍", "custom": "📦", "nvim": "󰹻"}']
    options = Options.from_options(server)
    assert get_program_icon('python', options) == '🐍'
    assert get_program_icon('custom', options) == '📦'
    assert get_program_icon('nvim', options) == '󰹻'


def test_substitute_name_folds_node_homebrew_cli():
    """Node CLI wrappers launched via Homebrew bin should fold to the CLI name."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name(
        'node --max-old-space-size=8192 --expose-gc /opt/homebrew/bin/openclaude',
        options.substitute_sets,
        options,
        True,
    )
    assert name == 'openclaude'


def test_substitute_name_folds_node_cli_absolute_node_path():
    """node itself is commonly an absolute path (Homebrew), e.g.
    `/opt/homebrew/opt/node/bin/node /opt/homebrew/bin/openclaude`."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name(
        '/opt/homebrew/opt/node/bin/node /opt/homebrew/bin/openclaude',
        options.substitute_sets,
        options,
        True,
    )
    assert name == 'openclaude'


def test_substitute_name_folds_node_linuxbrew_cli():
    """Same fold should cover Linuxbrew path layout."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name(
        'node /home/linuxbrew/.linuxbrew/bin/openclaude',
        options.substitute_sets,
        options,
        True,
    )
    assert name == 'openclaude'


def test_substitute_name_folds_node_cli_with_user_args():
    """User args after the launcher path should be preserved."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name(
        'node --expose-gc /opt/homebrew/bin/openclaude --dangerously-skip-permissions',
        options.substitute_sets,
        options,
        True,
    )
    assert name == 'openclaude --dangerously-skip-permissions'


def test_substitute_name_strips_homebrew_bin_path():
    """Programs run by absolute path (e.g. Homebrew bins) fold to the executable name."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name('/opt/homebrew/bin/btop', options.substitute_sets, options, True)
    assert name == 'btop'


def test_substitute_name_strips_bin_path_keeps_args():
    """Only argv[0]'s directory is stripped; arguments (even paths) are preserved."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name('/Users/me/.local/bin/lazygit --path /some/repo', options.substitute_sets, options, True)
    assert name == 'lazygit --path /some/repo'


def test_substitute_name_leaves_bare_command():
    """A command with no directory component is left untouched."""
    options = Options(icon_style=IconStyle.NAME)
    name, _ = substitute_name('btop', options.substitute_sets, options, True)
    assert name == 'btop'
