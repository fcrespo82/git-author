mkdir -p $HOME/.local/bin

ln -sf `realpath ./main.py` $HOME/.local/bin/git-set_author

echo "Please make sure there's a config.ini in this folder with your required profiles"