#!/bin/bash

VERSION="0.0.1"
VERSION_NAME="Alpha"
echo "Running installer version: $VERSION ~ $VERSION_NAME" 

set -e

# CLI flags
SKIP_PACKAGES=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-packages)
            SKIP_PACKAGES=true
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            break
            ;;
    esac
done

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: $0 should be run as sudo."
    echo "Exiting script."
    exit 1
fi

if [ "$SKIP_PACKAGES" = false ]; then
    if ! command -v git &>/dev/null; then
        echo "git not found - installing.."
        pacman -S --noconfirm git
    fi

    if ! command -v yay &>/dev/null; then
        echo "yay not found - installing.."
        sudo -u "$SUDO_USER" bash -c "
    cd /tmp
    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si --noconfirm
"
    fi
fi

PACMAN_PKGS=(
    kitty
    neovim
    plymouth
    htop
    fastfetch
    picom
    xcape
    brightnessctl
    xorg-xinput
    alsa-utils
    github-cli
    stow
    python-pip
    mypy
    gnome-keyring
    ttf-fira-code
    tui-journal
    python-pywal
)

AUR_PKGS=(
    brave-browser
    visual-studio-code-bin
)

PIP_PKGS=(
    qtile-extras
)


if [ "$SKIP_PACKAGES" = false ]; then
    echo "Updating system"
    pacman -Syu

    echo "Installing pacman packages"
    pacman -S --needed --noconfirm ${PACMAN_PKGS[@]}

    echo "Installing AUR packages"
    sudo -u "$SUDO_USER" bash -c "
yay -S --noconfirm ${AUR_PKGS[@]}
"

    echo "Installing Qtile-Extras"
    sudo -u "$SUDO_USER" bash -c "
pip install --user qtile-extras --break-system-packages
"

    echo ""
else
    echo "--skip-packages supplied; skipping package and AUR installation."
fi

sudo -u "$SUDO_USER" bash -c "
git clone https://github.com/stcoops/dotfiles.git
cd dotfiles
"
 
echo "WARNING: In order to correctly apply dotfiles we need to clean the .config directory"
echo "[B]ackup existing files (default), [D]elete only folders not in dotfiles, or [A]adopt current config into dotfiles using stow --adopt:"

# Determine the target user's home directory
if [ -n "$SUDO_USER" ]; then
    TARGET_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    TARGET_HOME="$HOME"
fi

DOTFILES_DIR="$TARGET_HOME/dotfiles"

read -rp "Choose option [B/D/A] (default B): " choice
choice=${choice:-B}
choice="${choice^^}"

case "$choice" in
    B)
        if [ -d "$TARGET_HOME/.config" ]; then
            ts=$(date +%Y%m%d%H%M%S)
            backup_dir="$TARGET_HOME/.config.backup.$ts"
            mv "$TARGET_HOME/.config" "$backup_dir"
            chown -R "$SUDO_USER":"$SUDO_USER" "$backup_dir" 2>/dev/null || true
            echo "Backed up .config to: $backup_dir"
        else
            echo "No .config directory to backup."
        fi
        ;;
    D)
        if [ -d "$TARGET_HOME/.config" ]; then
            if [ ! -d "$DOTFILES_DIR/.config" ]; then
                echo "No '.config' package found in $DOTFILES_DIR; nothing will be deleted."
            else
                for entry in "$TARGET_HOME/.config"/*; do
                    [ -e "$entry" ] || continue
                    name=$(basename "$entry")
                    if [ ! -e "$DOTFILES_DIR/.config/$name" ]; then

                        echo "Kept $entry (found in dotfiles)"
                    
                    else

                        rm -rf "$entry"
                        echo "Deleted $entry (not present in dotfiles)"
                    fi
                done
            fi
        else
            echo "No .config directory to process."
        fi
        ;;
    A)
                        echo "Kept $entry (found in dotfiles)"
        if [ -d "$TARGET_HOME/.config" ]; then
            mkdir -p "$DOTFILES_DIR"
            # Ensure there is a package directory for stow to adopt into
            mkdir -p "$DOTFILES_DIR/config"
            chown -R "$SUDO_USER":"$SUDO_USER" "$DOTFILES_DIR" 2>/dev/null || true
            echo "Adopting existing .config into $DOTFILES_DIR/config using stow --adopt"
            sudo -u "$SUDO_USER" bash -c "cd \"$DOTFILES_DIR\" && stow --adopt --target=\"$TARGET_HOME\" config" || true
            echo "Adopt step complete — review $DOTFILES_DIR/config and commit to your dotfiles repo."
        else
            echo "No .config directory to adopt."
        fi
        ;;
    *)
        echo "Invalid choice. Skipping .config handling."
        ;;
esac

# Now run stow to symlink all packages from the dotfiles repo (if present)
sudo -u "$SUDO_USER" bash -c "
cd \"$DOTFILES_DIR\"
stow .
"

echo "Installation Complete"
