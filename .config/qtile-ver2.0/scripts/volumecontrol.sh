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

elif [ "$1" == "get" ]; then
    AMIXER_OUT=$(amixer get Master 2>/dev/null)
    # extract first percentage and return numeric value (no %), fallback to 0 if not found
    PCT=$(echo "$AMIXER_OUT" | grep -o -m1 '[0-9]\+%')
    if [ -z "$PCT" ]; then
        PCT_NUM=0
    else
        PCT_NUM="${PCT%\%}"
    fi

    # detect muted/off state (some mixers use [off], others [muted])
    if echo "$AMIXER_OUT" | grep -qiE '\[(off|muted)\]'; then
        MUTE_STATE="mute"
    else
        MUTE_STATE="unmute"
    fi

    # Output: first line = percentage (numeric), second line = "mute" or "unmute"
    echo "$PCT_NUM"
    echo "$MUTE_STATE"
    exit 0


elif [ "$1" == "set" ] && [ -n "$2" ]; then
    # Set volume to specific percentage value
    amixer sset Master "$2"% 2>/dev/null && exit 0


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