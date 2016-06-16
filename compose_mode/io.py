#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Functions for reading and writing mostly the state file and modes file. """
import os

import yaml

from compose_mode import exceptions


DEFAULT_MODES_FILE = 'compose-modes.yml'
STATE_FILE = '.compose-mode.state'


def _search_up(filename, stop_at_git=True):
    prefix = ''
    while True:
        path = os.path.join(prefix, filename)

        if os.path.isfile(path):
            return path
        elif prefix == '/' or (os.path.isdir(os.path.join(prefix, '.git')) and
                               stop_at_git):
            # insisting that .git is a dir means we will traverse out of git
            # submodules, a behaviour I desire
            raise exceptions.ComposeModeYmlNotFound(
                '{} not found here or any directory above here'
                .format(filename)
            )
        prefix = os.path.realpath(os.path.join(prefix, '..'))


def get_modes(modes_filename=DEFAULT_MODES_FILE):
    """ Returns the dict read in from the yaml modes file.

    This is what generates the "modes" variable you'll see around the rest of this file.
    """
    modes_path = _search_up(modes_filename)
    with open(modes_path, 'r') as modes_file:
        return os.path.realpath(modes_path), yaml.safe_load(modes_file)


def get_current_mode():
    try:
        with open(STATE_FILE, 'r') as state_file:
            return state_file.read().strip()
    except IOError:
        return None


def set_current_mode(mode):
    """ Set the mode cached in the state file

    Notably doesn't actually change the mode, should only be called when the mode is changed in set_mode.
    """
    with open(STATE_FILE, 'w') as state_file:
        state_file.write(mode)


def main():
    pass

if __name__ == '__main__':
    main()
