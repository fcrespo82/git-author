# README git set_author

Easily set git commit author for your **personal**, **work** or any other profile requirements.

## Installation

Make sure python scripts path is in your `PATH`.

```shell
pip install git+https://github.com/fcrespo82/git-set_author.git
```

## Usage

```
Usage: git-author [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help     Show this message and exit.
  --config PATH  The config file to use.  [default: ~\git-authors.conf]

Commands:
  edit
  list
  set
```

Every command has a help flag (-h/--help) to list its options.

- `edit`: Edit profiles file or create one if it doesn't exists.
- `list`: List profiles, use `-v` to show its values.
- `set`: Sets a profile. MUST be in a git directory to work.

## Configuration

```shell
git author [--config file.ini] edit 
```

This command will open an editor with a template and save it in a file named `git-authors.conf` or the file you passed in the options.

### Supported params

- name
- email
- signingkey


## Usage

```shell
git author set [profile]
```

Upon setting a profile, if it has the `signingkey` value, it will automatically set `commit.gpgsign` to `true`