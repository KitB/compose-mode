#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import os
import sys

import compose_mode
from compose_mode import exceptions, generate, io, status

logging.basicConfig()


NO_CONFIG_HELP = """
No configuration file "{}" was found within the search path.

It is recommended that you create this file at the root of your git repository
(compose-mode will not traverse out of a git repository, though it will traverse
out of submodules and into their parent).
""".lstrip()


def set_mode(args):
    """ This is where the real functionality is

    TODO: Pull this out into functions a bit more.
    """
    # Grab the bits out of args
    output = args.output
    selected_mode = args.mode
    modes_file = args.modes_file

    # Figure out and normalize the context we're working in
    try:
        modes_path, modes = io.get_modes(modes_file)
    except exceptions.ComposeModeYmlNotFound:
        print NO_CONFIG_HELP.format(modes_file)
        return 1

    containing_dir = os.path.dirname(modes_path)

    os.chdir(containing_dir)  # Easier than trying to join the paths up properly

    # Handle the arguments/options for printing out the current status
    # (These will halt execution)
    if args.machine_readable or args.json:
        status.handle_machine_readable_status(modes, output, containing_dir, args.json)
        return 0
    elif selected_mode == 'list':
        status.handle_list(modes, output, containing_dir)
        return 0

    # Generate the configuration
    output_configuration = generate.configuration(selected_mode, modes, containing_dir)

    # Write out the files (docker-compose.yml and .compose-mode.state)
    with open(output, 'w') as output_file:
        output_file.write(output_configuration)
    io.set_current_mode(selected_mode)

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-V', action='version',
                        version='%(prog)s {}'.format(compose_mode.__version__))
    parser.add_argument('--modes-file', default=io.DEFAULT_MODES_FILE,
                        help='The name or path of the modes file, will search'
                             ' in containing directories if a relative name is'
                             ' given')
    parser.add_argument('--machine-readable', action='store_true',
                        help='Output the status in easy machine parseable format then exit')
    parser.add_argument('--json', action='store_true',
                        help='Output the status in json then exit')
    parser.add_argument(
        '--output', default='docker-compose.yml',
        help='The file to output the effective configuration to')

    parser.add_argument('mode', nargs='?', default='list',
                        help='The mode to switch to, leave blank or set to '
                             '"list" to list available modes.')

    args = parser.parse_args()

    exit_code = set_mode(args)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
