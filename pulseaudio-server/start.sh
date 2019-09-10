#!/bin/bash

# TBD
cp /etc/pulse/default_without_alsa_sinks_and_sources.pa /etc/pulse/default.pa
echo "# adding alsa sinks/sources configured by env vars alsa-sinkN and alsa-sourceN :"
if [ $alsa-sink1 != "" ]; then
   echo "load-module module-alsa-sink $alsa-sink1" >> /etc/pulse/default.pa
fi

if [ $alsa-source1 != "" ]; then
   echo "load-module module-alsa-source $alsa-source1" >> /etc/pulse/default.pa
fi

# run bluetooth connect loop
/connect_bluetooth.sh &

echo starting pulseaudio ...
pulseaudio --log-level=4
echo ERROR: pulseaudio stopped
