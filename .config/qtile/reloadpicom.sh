#!bin/bash

# check if picom is running 
if pgrep -x "picom" > /dev/null
then
    # if picom is running, kill it
    pkill picom
    # wait for a moment to ensure picom has stopped
    sleep 0.5
fi

picom -b