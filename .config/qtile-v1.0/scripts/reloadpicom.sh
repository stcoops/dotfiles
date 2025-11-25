#!bin/bash

# check if picom is running 
if pgrep -x "picom" > /dev/null
then
    # if picom is running, kill it
    pkill picom
fi

picom -b