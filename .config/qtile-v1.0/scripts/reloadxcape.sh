#!/bin/bash
# check if xcape is running
if pgrep -x "xcape" > /dev/null
then
    # if xcape is running, kill it
    pkill xcape
fi
setxkbmap -option # Reset any conflicting options
xcape -e 'Super_L=XF86MyComputer'