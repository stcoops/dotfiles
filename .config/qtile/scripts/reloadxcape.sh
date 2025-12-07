#!/bin/bash
# check if xcape is running
if pgrep -x "xcape" > /dev/null
then
    # if xcape is running, kill it
    pkill -x xcape
fi
setxkbmap -option # Reset any conflicting options

xmodmap -pke | grep -q 'F13' || xmodmap -e 'keycode 255 = F13'

xcape -t 200 -e 'Super_L=F13'