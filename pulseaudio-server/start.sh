#!/bin/bash

# TBD
cp /etc/pulse/default_without_alsa_sinks_and_sources.pa /etc/pulse/default.pa

# run bluetooth connect loop
/connect_bluetooth.sh &

echo starting pulseaudio ...
pulseaudio --log-level=4
echo ERROR: pulseaudio stopped
