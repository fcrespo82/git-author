import configparser
import os
import subprocess

import click
from tabulate import tabulate


def is_git():
    return subprocess.run(['git', 'status'], check=False,
                          capture_output=True).returncode == 0


@click.group()
@click.help_option("-h", "--help")
@click.option("--config", type=click.Path(), default=os.path.join(os.path.expanduser("~"), "git-set-author.ini"), help="The config file to use.", show_default=True)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["path"] = config
    config_obj = configparser.ConfigParser()
    config_obj.read(config)
    ctx.obj["parser"] = config_obj


@cli.command()
@click.help_option("-h", "--help")
@click.option("--editor", type=click.Path(), help="Editor to use, uses EDITOR environment variable", envvar="EDITOR")
@click.pass_context
def edit(ctx, editor):
    marker = ("# Everything below this line is ignored",
              """[personal_profile] # You can change this name to anything you want
name=My name
email=email@gmail.com

[work_profile]
name=My professional name
email=email@work.com
signingkey=7439487398473948""")

    if not os.path.exists(ctx.obj["path"]):
        text = click.edit("\n\n" + "\n".join(marker),
                          editor=editor, extension="ini")
        text = text.split(marker[0], 1)[0].rstrip("\n")
        with open(ctx.obj["path"], mode="w", encoding="utf8") as _file:
            _file.write(text)
    else:
        click.edit(filename=ctx.obj["path"], editor=editor)


@cli.command()
@click.help_option("-h", "--help")
@click.option("-v", "--show_values", is_flag=True, type=bool, help="Show profile values")
@click.option("--tablefmt", default="rounded_outline", show_default=True, help="How to display the parameter list. Any option from python module 'tabulate'")
@click.pass_context
def list(ctx, tablefmt, show_values):
    for section in ctx.obj["parser"].sections():
        click.secho(section, fg="green")
        if show_values:
            data = map(lambda x: [click.style(x, fg="red"),
                                  ctx.obj["parser"][section][x]], ctx.obj["parser"][section])
            click.echo(
                tabulate(data, tablefmt=tablefmt, colalign=["right", "left"]))


def validate_set_profile(ctx, param, value):
    if not value in ctx.obj["parser"].sections():
        raise click.BadArgumentUsage(
            f"{param.name.upper()} should be one of {', '.join(map(lambda x: x, ctx.obj['parser'].sections()))}")
    return value


def setup_git(config, profile):
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
    subprocess.run(command_name, check=False)
    subprocess.run(command_email, check=False)
    if command_signing_key:
        subprocess.run(command_signing_key, check=False)
        subprocess.run(command_sign_commit, check=False)
    else:
        subprocess.run(command_signing_key_unset, check=False)
        subprocess.run(command_sign_commit_unset, check=False)


@cli.command()
@click.help_option("-h", "--help")
@click.argument("profile", callback=validate_set_profile)
@click.pass_context
def set(ctx, profile):
    if not is_git():
        click.secho(
            'You need to run this command inside a git repository', fg="red")
        exit()
    setup_git(ctx.obj["parser"], profile)


if __name__ == '__main__':
    cli()
