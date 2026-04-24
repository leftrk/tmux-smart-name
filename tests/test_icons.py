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
