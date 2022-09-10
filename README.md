# README git set_author

Easily set git commit author for your **personal**, **work** or any other profile requirements.

## Instalation

It will clone the repo and install a symbolic link in `$HOME/.local/bin`. If that folder does not exists it will create. Make sure this path is in your `PATH`.

```shell
git clone https://github.com/fcrespo82/git-set_author.git
cd git-set_author
./install.sh
```

## Configuration

Create a file named `config.ini` in the format of `config.ini.template` with your desired profiles.

## Usage

```shell
git set_author [profile]
```
