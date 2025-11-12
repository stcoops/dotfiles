#!/bin/bash

# NOTE: This script requires 'brightnessctl' to be installed and
# has been vibe-coded as fuck so be aware - IF I AM READING THIS THEN REWRITE ME!!!!!!
# (Probably works perfectly and better than my own code but IT'S THE PRINCIPLE!)


# Cycle keyboard backlight through discrete steps derived from device max.
# Usage: ./kbd_brightness.sh

set -euo pipefail

# Find first keyboard backlight device name (unquoted)
kbd_backlight_device=$(brightnessctl -l | grep -i 'kbd_backlight' | awk -F"'" '{print $2}' | head -n1)
if [ -z "$kbd_backlight_device" ]; then
    echo "No keyboard backlight device found."
    exit 1
fi

# Query numeric brightness values (absolute units used by the device)
CURRENT_BRIGHTNESS=$(brightnessctl -d "$kbd_backlight_device" get 2>/dev/null || true)
MAX_BRIGHTNESS=$(brightnessctl -d "$kbd_backlight_device" max 2>/dev/null || true)

if [ -z "$CURRENT_BRIGHTNESS" ] || [ -z "$MAX_BRIGHTNESS" ] || [ "$MAX_BRIGHTNESS" -le 0 ]; then
    echo "Keyboard backlight control not available."
    exit 1
fi

# If the device uses only a few discrete steps (e.g. max=2 -> levels 0,1,2),
# mapping percentages will often collide. Compute two intermediate step thresholds
# using integer (ceiling) division so we cycle through distinct numeric levels.

# step1 = ceil(MAX/3), step2 = ceil(2*MAX/3)
step1=$(( (MAX_BRIGHTNESS + 2) / 3 ))
step2=$(( (2 * MAX_BRIGHTNESS + 2) / 3 ))

current=$((CURRENT_BRIGHTNESS))
target=0

if [ "$current" -lt "$step1" ]; then
    target=$step1
elif [ "$current" -lt "$step2" ]; then
    target=$step2
elif [ "$current" -lt "$MAX_BRIGHTNESS" ]; then
    target=$MAX_BRIGHTNESS
else
    target=0
fi

# Apply the numeric target (no percent sign) so we move between 0..MAX_BRIGHTNESS levels
if brightnessctl -d "$kbd_backlight_device" set "$target" >/dev/null 2>&1; then
    echo "Set device '$kbd_backlight_device' to $target (of $MAX_BRIGHTNESS)"
    exit 0
else
    echo "Failed to set keyboard backlight for device '$kbd_backlight_device'"
    exit 1
fi