#!/bin/bash

# TBD
cp /etc/pulse/default_without_alsa_sinks_and_sources.pa /etc/pulse/default.pa
echo "# adding alsa sinks/sources configured by env vars alsa-sinkN and alsa-sourceN :" >> /etc/pulse/default.pa
if [ "$alsa_sink1" != "" ]; then
   echo "load-module module-alsa-sink $alsa_sink1" >> /etc/pulse/default.pa
fi

if [ "$alsa_source1" != "" ]; then
   echo "load-module module-alsa-source $alsa_source1" >> /etc/pulse/default.pa
fi

# run bluetooth connect loop
/connect_bluetooth.sh &

echo starting pulseaudio ...
pulseaudio --log-level=4
echo ERROR: pulseaudio stopped
