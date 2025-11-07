#!/bin/bash

# This script adjusts the screen brightness.
# Usage: ./brightness.sh [up/down]
# 'up' increases brightness by 10%
# 'down' decreases brightness by 10%

# Check if brightnessctl is installed

if [ "$1" == "up" ]; then
    out=$(brightnessctl set +10% 2>/dev/null)

elif [ "$1" == "down" ]; then
    # ignore if brightness is already at minimum (10%)
    CURRENT_BRIGHTNESS=$(brightnessctl get 2>/dev/null)
    MAX_BRIGHTNESS=$(brightnessctl max 2>/dev/null)
    CURRENT_PERCENT=$((CURRENT_BRIGHTNESS * 100 / MAX_BRIGHTNESS))
    if [ $CURRENT_PERCENT == 10 ]; then
        exit 0
    fi
    out=$(brightnessctl set 10%- 2>/dev/null)

fi

if [ -n "$out" ]; then  
    echo "$out"
fi


