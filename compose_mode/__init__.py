#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os

from compose import config
from compose.config import serialize
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
        return os.path.realpath(modes_path), yaml.safe_load(modes_file)


def fix_restart(restart_config):
    mrc = restart_config['MaximumRetryCount']
    name = restart_config['Name']

    if name in ['always', 'unless-stopped', 'no']:
        return name
    else:
        return '{}:{}'.format(name, mrc)


def fix_restarts(input_yaml):
    config_dict = yaml.safe_load(input_yaml)
    for service in config_dict['services'].itervalues():
        try:
            service['restart'] = fix_restart(service['restart'])
        except KeyError:
            pass
    return yaml.safe_dump(config_dict,
                          default_flow_style=False,
                          indent=4,
                          width=80)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--modes-file', default=DEFAULT_MODES_FILE,
                        help='The name or path of the modes file, will search'
                             ' in containing directories if a relative name is'
                             ' given')
    parser.add_argument(
        '--output', default='docker-compose.yml',
        help='The file to output the effective configuration to')

    parser.add_argument('mode', nargs='?', default='list')

    args, remaining_args = parser.parse_known_args()

    modes_path, modes = get_modes(args.modes_file)

    if args.mode == 'list':
        print '\n'.join(sorted(modes.iterkeys()))
        return

    containing_dir = os.path.dirname(modes_path)

    # Easier than trying to join the paths up properly
    os.chdir(containing_dir)

    # project_name = os.path.basename(containing_dir)
    config_details = config.find(containing_dir, modes[args.mode])
    loaded_config = config.load(config_details)

    broken_serialized = serialize.serialize_config(loaded_config)
    fixed_serialized = fix_restarts(broken_serialized)

    with open(args.output, 'w') as output_file:
        output_file.write(fixed_serialized)

if __name__ == '__main__':
    main()
