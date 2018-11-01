import json

from compose_mode import generate, io


def get_current_mode_up_to_date(current_mode_config, output_file):
    with open(output_file, 'r') as output_f:
        actual_current = output_f.read()
    return actual_current == current_mode_config


def handle_list(modes, output_file, containing_dir):
    """ Print the available modes and which one we're in

    *and* tell us if it's out of date.

    `compose-mode list` will bring us down this path
    """
    current_mode = io.get_current_mode()

    for mode in sorted(modes.keys()):
        print(mode, end=' ')  # comma prevents newline
        if mode == current_mode:
            print('*', end=' ')
            current_mode_config = generate.configuration(
                mode,
                modes,
                containing_dir
            )
            if not get_current_mode_up_to_date(
                    current_mode_config,
                    output_file):
                print('Out of date!', end=' ')
        print()


def handle_machine_readable_status(modes, output_file, containing_dir, print_json=False):
    """ Print out the current mode and whether it's dirty

    --machine-readable and --json will put us here
    """
    current_mode = io.get_current_mode()
    current_mode_config = generate.configuration(
        current_mode,
        modes,
        containing_dir
    )

    dirty = not get_current_mode_up_to_date(current_mode_config, output_file)

    if not print_json:
        dirty_str = 'y' if dirty else 'n'
        print('{} {}'.format(current_mode, dirty_str))
    else:
        print(json.dumps({'mode': current_mode, 'dirty': dirty}))
