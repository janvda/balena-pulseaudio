#!/bin/bash

# run bluetooth connect loop
/connect_bluetooth &

echo starting pulseaudio ...
pulseaudio --log-level=4
echo ERROR: pulseaudio stopped
