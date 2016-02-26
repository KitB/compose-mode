#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os

import yaml


DEFAULT_MODES_FILE = 'compose-modes.yml'


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
            raise IOError('{} not found here or any directory above here'
                          .format(filename))
        prefix = os.path.realpath(os.path.join(prefix, '..'))


def get_modes(modes_filename=DEFAULT_MODES_FILE):
    modes_path = _search_up(modes_filename)
    with open(modes_path, 'r') as modes_file:
        return yaml.safe_load(modes_file)


def construct_f_args(modes, chosen_mode):
    yml_list = modes[chosen_mode]
    return ' '.join('-f {}'.format(yml) for yml in yml_list).split()


def run_compose(binary_path, modes, chosen_mode, args):
    f_args = construct_f_args(modes, chosen_mode)
    os.execv(binary_path, ['docker-compose'] + f_args + args)


def main():
    # Find docker-compose
    compose_binary_path = os.popen('which docker-compose').read().strip()

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--modes-file', default=DEFAULT_MODES_FILE,
                        help='The name or path of the modes file, will search'
                             ' in containing directories if a relative name is'
                             ' given')

    parser.add_argument('--compose-binary',
                        default=compose_binary_path,
                        required=not compose_binary_path,  # False if ''
                        help='Where to find compose')

    parser.add_argument('mode')

    args, remaining_args = parser.parse_known_args()

    modes = get_modes(args.modes_file)
    run_compose(args.compose_binary, modes, args.mode, remaining_args)

if __name__ == '__main__':
    main()
