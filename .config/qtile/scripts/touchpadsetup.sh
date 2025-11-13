
#!bin/bash
# Find the touchpad device id and set libinput properties.
# If invoked with "reset" it will disable/enable the device and re-apply the settings.

# Find a likely touchpad line from `xinput list`
device_line=$(xinput list 2>/dev/null | grep -i -E 'touchpad|touch pad|synaptics|trackpad' | head -n1 || true)
if [ -z "$device_line" ]; then
    echo "No touchpad device found via xinput."
    exit 1
fi

# Extract the numeric id from the line (e.g. id=14)
device_id=$(echo "$device_line" | sed -n 's/.*id=\([0-9]\+\).*/\1/p')
if [ -z "$device_id" ]; then
    echo "Failed to parse device id from: $device_line"
    exit 1
fi

# If "reset" was requested, restart the device (disable -> enable)
if [ "$1" == "reset" ]; then
    xinput disable "$device_id"
    sleep 0.2
    xinput enable "$device_id"
fi

# Apply desired settings
xinput set-prop "$device_id" "libinput Tapping Enabled" 1
xinput set-prop "$device_id" "libinput Natural Scrolling Enabled" 1
xinput set-prop "$device_id" "libinput Disable While Typing Enabled" 0

exit 0