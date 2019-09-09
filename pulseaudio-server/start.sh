#!/bin/bash

# run bluetooth connect loop
/connect_bluetooth.sh &

echo starting pulseaudio ...
pulseaudio --log-level=4
echo ERROR: pulseaudio stopped
