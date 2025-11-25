#!/bin/bash

kbd_backlight_device=$(brightnessctl -l | grep -i 'kbd_backlight' | awk -F"'" '{print $2}' | head -n1)
if [ -z "$kbd_backlight_device" ]; then
    echo "No keyboard backlight device found."
    exit 1
fi

CURRENT_BRIGHTNESS=$(brightnessctl -d "$kbd_backlight_device" get 2>/dev/null || true)
MAX_BRIGHTNESS=$(brightnessctl -d "$kbd_backlight_device" max 2>/dev/null || true)

# Define possible brightness levels as steps from 0 to MAX_BRIGHTNESS
# so in this case of 2 levels we have 0, 1, 2
# and in case of 3 levels we have 0, 1, 2, 3 etc.

mapfile -t BRIGHTNESS_LEVELS < <(seq 0 "$MAX_BRIGHTNESS")
echo "${BRIGHTNESS_LEVELS[@]}" | tr ' ' '\n' 

if [ "$1" == "set" ]; then
    NEW_BRIGHTNESS=$((CURRENT_BRIGHTNESS + 1))
    brightnessctl -d "$kbd_backlight_device" set  >/dev/null 2>&1
    if [ "$NEW_BRIGHTNESS" -gt "$MAX_BRIGHTNESS" ]; then
        NEW_BRIGHTNESS=0
    fi

    brightnessctl -d "$kbd_backlight_device" set "$NEW_BRIGHTNESS" #>/dev/null 2>&1


elif [ "$1" == "get" ]; then
    echo "$CURRENT_BRIGHTNESS"
    echo "$MAX_BRIGHTNESS"

fi