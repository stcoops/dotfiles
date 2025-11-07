#!/bin/bash

# This script adjusts the amixer volume.
# Usage: ./volumecontrol.sh [up/down/mute]
# 'up' increases volume by 5%
# 'down' decreases volume by 5%
# 'mute' toggles mute


if [ "$1" == "up" ]; then
    amixer sset Master 5%+ 2>/dev/null && exit 0
elif [ "$1" == "down" ]; then
    amixer sset Master 5%- 2>/dev/null && exit 0


elif [ "$1" == "mute" ]; then
    CURRENT_STATE=`amixer get Master | grep -E 'Playback.*?\[o' | grep -E -o '\[o.+\]'`

    if [[ $CURRENT_STATE == '[on]' ]]; then
        amixer sset Master mute
    else
        amixer sset Master unmute
        amixer sset Speaker unmute
        if amixer sget 'Headphone' &>/dev/null; then
            amixer sset 'Headphone' unmute
        fi
    fi
fi