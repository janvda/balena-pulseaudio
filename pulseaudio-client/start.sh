#!/bin/bash

# see https://github.com/janvda/balena-pulseaudio/issues/13
unset DISPLAY

echo "Listing all sinks (= playback devices):"
pactl list sinks short

echo "Listing all sources (= audio capture devices):"
pactl list sources short | grep -v ".monitor"

if [ "$default_sink" != "" ]; then
   echo "Set default sink to $default_sink"
   pactl set-default-sink $default_sink
fi

if [ "$default_source" != "" ]; then
   echo "Set default source to $default_source"
   pactl set-default-source $default_source
fi

echo "Listing default sink and source"
pactl info | grep "Sink\|Source"

case $test_id in
"") echo "INFO: You can specify a specific test by setting \$test_id."
   ;;
0) ;;
1) echo "running test 1 - play audio file using paplay :"
   paplay LRMonoPhase4.wav
   echo "... end of test 1"
   ;;
2) echo "running test 2: "
   echo "- Started recording audio for 10 seconds ..."
   parecord --channels=1 record_session1.wav &
   sleep 10
   kill $!  #$! expands to the PID of the last process executed in the background
   echo "- Playing recorded audio..."
   paplay record_session1.wav
   echo "... end of test 2"
   ;;
*) echo "ERROR: \$test_id (= $test_id) has not a valid value".
esac

echo "sleeping forever ..."
while true; do
   # every hour a "zzz" is put into the log files.
   echo "    zzz"
   sleep 3600
done



echo -e "STEP 4: Sleeping forever"
