#!/bin/bash

# Test script for controlling all brightnessctl lights, asside from the monitor backlight
# Requires brightnessctl to be installed and configured properly

# Function to test brightness control for a given device
# Extract the device name quoted by brightnessctl (e.g. 'platform::mute')
# and skip any backlight entries.
DEVICES=$(brightnessctl --list | grep -v 'backlight' | awk -F"'" '/Device/ {print $2}')
echo "devices:"
for d in $DEVICES; do
	echo " - $d"
	# Get device info and parse current/max brightness
	info=$(brightnessctl -d "$d" info 2>/dev/null)
	if [ -z "$info" ]; then
		echo "   -> unable to read info for $d"
		continue
	fi
	cur=$(echo "$info" | awk '/Current/ {for(i=1;i<=NF;i++) if ($i ~ /[0-9]+/) {print $i; exit}}' | grep -oE '[0-9]+' )
	max=$(echo "$info" | awk '/Max/ {for(i=1;i<=NF;i++) if ($i ~ /[0-9]+/) {print $i; exit}}' | grep -oE '[0-9]+' )
	# Fallbacks if parsing failed
	if [ -z "$cur" ]; then
		cur=$(brightnessctl -d "$d" get 2>/dev/null | tr -d '\n')
	fi
	if [ -z "$max" ]; then
		max=$(brightnessctl -d "$d" max 2>/dev/null | tr -d '\n')
	fi
	if [ -z "$cur" ] || [ -z "$max" ]; then
		echo "   -> cannot determine brightness for $d (cur:$cur max:$max)"
		continue
	fi
	echo "   -> current: $cur  max: $max"

	# Toggle: set to max, wait 0.2s, set to min
	echo "   -> setting $d to max ($max)"
	brightnessctl -d "$d" set "$max" >/dev/null 2>&1 || echo "     (set to $max failed)"
	sleep 0.2
	echo "   -> setting $d to min (0)"
	brightnessctl -d "$d" set 0 >/dev/null 2>&1 || echo "     (set to 0 failed)"

	# 1 second gap before next device
	sleep 1
done