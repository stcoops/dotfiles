# Dotfiles

Minimal, portable configs for qtile, picom, kitty, and more.

## Overview
Keep source files in this repo and symlink or install them to $HOME so configs can be reused across machines.

## Quick install
1. Clone:
```bash
git clone https://github.com/stcoops/dotfiles.git ~/dotfiles
cd ~/dotfiles
```
2. use GNU Stow:
```bash
stow -t $HOME zsh nvim git tmux
```

## Structure
Typical repo layout:
```
~/dotfiles
├── README.md
├── .gitignore
└── .config
    ├── kitty
    │   └── kitty.conf
    ├── picom
    │   └── picom.conf
    ├── qtile
    │   ├── brightness.sh
    │   ├── colorschemes.py
    │   ├── config.py
    │   ├── kbd_brightness.sh
    │   ├── reloadpicom.sh
    │   └── volumecontrol.sh
    └── wallpapers
        └── wp12821730.jpg
```

## Usage
- Edit files in their folders (.config/xx)
- Re-run install.sh or stow after changes.
- Keep repo synced with `git pull` and commit local edits.
