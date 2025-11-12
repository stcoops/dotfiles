# Dotfiles

Minimal, portable configs for qtile, picom, kitty, and more.

## Overview
Keep source files in this repo and symlink or install them to $HOME so configs can be reused across machines.

## Quick install
1. Clone:
```bash
git clone https://github.com/stcoops/dotfiles.git ~/dotfiles
```
2. Use Stow (recommended, see [GNU Stow](https://www.gnu.org/software/stow/) for more):
```bash
# Debian/Ubuntu
sudo apt install stow

# macOS (Homebrew)
brew install stow

# Arch (btw!)
sudo pacman -S stow
```
```bash
stow ~/dotfiles
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
- Edit files in their folders (e.g. .config//kitty/kitty.conf)
- Re-run `stow ~/dotfiles` after changes.
- Keep repo synced with `git pull` and commit local edits.
