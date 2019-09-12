#!/bin/bash

echo "# adding alsa sinks configured by environment variables alsa_sink1, alsa_sink2, alsa_sink3 :" >> /etc/pulse/default.pa
if [ "$alsa_sink1" != "" ]; then
   echo "load-module module-alsa-sink $alsa_sink1" >> /etc/pulse/default.pa
fi
if [ "$alsa_sink2" != "" ]; then
   echo "load-module module-alsa-sink $alsa_sink2" >> /etc/pulse/default.pa
fi
if [ "$alsa_sink3" != "" ]; then
   echo "load-module module-alsa-sink $alsa_sink3" >> /etc/pulse/default.pa
fi

echo "# adding alsa sources configured by environment variables alsa_source1, alsa_source2, alsa_source3 :" >> /etc/pulse/default.pa
if [ "$alsa_source1" != "" ]; then
   echo "load-module module-alsa-source $alsa_source1" >> /etc/pulse/default.pa
fi
if [ "$alsa_source2" != "" ]; then
   echo "load-module module-alsa-source $alsa_source2" >> /etc/pulse/default.pa
fi
if [ "$alsa_source3" != "" ]; then
   echo "load-module module-alsa-source $alsa_source3" >> /etc/pulse/default.pa
fi

# run bluetooth connect loop
/connect_bluetooth.sh &

echo starting pulseaudio ...
pulseaudio --system --log-level=4
echo ERROR: pulseaudio stopped
