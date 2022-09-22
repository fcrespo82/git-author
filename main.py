#!/usr/bin/env python
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import configparser
import os
import subprocess
from argparse import ArgumentParser

python_script_dir = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(python_script_dir, 'config.ini'))


def setup_parser():
    parser = ArgumentParser()
    parser.add_argument('profile', type=str, choices=config.sections())
    return parser.parse_args()


def setup_git(profile):
    command_name = ['git', 'config', '--local',
                    'user.name', config[profile]['name']]
    command_email = ['git', 'config', '--local',
                     'user.email', config[profile]['email']]
    command_signing_key = None
    if 'signingkey' in config[profile]:
        command_signing_key = ['git', 'config', '--local',
                               'user.signingkey', config[profile]['signingkey']]
    command_signing_key_unset = ['git', 'config',
                                 '--local', '--unset', 'user.signingkey']

    is_git = subprocess.run(['git', 'status'], check=False,
                            capture_output=True).returncode == 0

    if is_git:
        subprocess.run(command_name, check=False)
        subprocess.run(command_email, check=False)
        if command_signing_key:
            subprocess.run(command_signing_key, check=False)
        else:
            subprocess.run(command_signing_key_unset, check=False)
    else:
        print('Not a git repository')


if __name__ == '__main__':
    args = setup_parser()
    setup_git(args.profile)
