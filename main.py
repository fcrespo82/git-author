#!/usr/bin/env python
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import configparser
import os
import subprocess
from argparse import ArgumentParser

python_script_dir = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
CONFIG_PATH = os.path.join(python_script_dir, 'config.ini')
TEMPLATE_CONFIG_PATH = os.path.join(python_script_dir, 'config.ini.template')
config.read(CONFIG_PATH)


def setup_parser():
    arg_parser = ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--set', type=str,
                       choices=config.sections(), required=False,
                       help='Set the git author to be one of the configured profiles')
    group.add_argument('-e', '--edit', action='store_true', required=False,
                       help='Open a text editor to configure the profiles')
    group.add_argument('-l', '--list', action='store_true', help='List available config choices with params')
    return arg_parser


def is_git():
    return subprocess.run(['git', 'status'], check=False,
                          capture_output=True).returncode == 0


def setup_git(profile):
    command_name = ['git', 'config', '--local',
                    'user.name', config[profile]['name']]
    command_email = ['git', 'config', '--local',
                     'user.email', config[profile]['email']]
    command_signing_key = []
    command_sign_commit = []
    if 'signingkey' in config[profile]:
        command_signing_key = ['git', 'config', '--local',
                               'user.signingkey', config[profile]['signingkey']]
        command_sign_commit = ['git', 'config',
                               '--local', 'commit.gpgsign', 'true']
    command_signing_key_unset = ['git', 'config',
                                 '--local', '--unset', 'user.signingkey']
    command_sign_commit_unset = ['git', 'config',
                                 '--local', '--unset', 'commit.gpgsign']
    if is_git():
        subprocess.run(command_name, check=False)
        subprocess.run(command_email, check=False)
        if command_signing_key:
            subprocess.run(command_signing_key, check=False)
            subprocess.run(command_sign_commit, check=False)
        else:
            subprocess.run(command_signing_key_unset, check=False)
            subprocess.run(command_sign_commit_unset, check=False)
    else:
        print('Not a git repository')


def edit_file():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='UTF-8') as empty_config:
            with open(TEMPLATE_CONFIG_PATH, 'r', encoding='UTF-8') as template_config:
                empty_config.writelines(template_config.readlines())

    import sys
    platform = sys.platform
    editor = 'vim'
    if platform == 'linux':
        editor = 'vim'
    elif platform == 'win32':
        editor = 'notepad.exe'

    if 'EDITOR' in os.environ:
        editor = os.environ['EDITOR']

    subprocess.run(editor.split(' ') + [CONFIG_PATH], check=True)

def list_choices():
    for section in config.sections():
        mapped = '\n'.join(map(lambda x: f'{x}={config[section][x]}', config[section])).replace('=','\t')
        print(f'''\n[{section}]
{mapped}''')

if __name__ == '__main__':
    if not is_git():
        print('You need to run this command inside a git repository')
        exit(1)
    parser = setup_parser()
    args = parser.parse_args()
    if args.edit:
        edit_file()
        exit(2)
    elif args.set:
        setup_git(args.set)
    elif args.list:
        list_choices()
    else:
        parser.print_help()
