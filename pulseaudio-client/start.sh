#!/bin/bash

# see https://github.com/janvda/balena-pulseaudio/issues/13
unset DISPLAY

echo "Listing all sinks (= playback devices):"
pactl list sinks short

echo "Listing all sources (= audio capture devices):"
pactl list sources short

case $test_id in
"") ;;
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
*) echo "\$test_id = $test_id is not a valid value".
esac

while true; do
   # every hour a "zzz" is put into the log files.
   echo "    zzz"
   sleep 3600
done



echo -e "STEP 4: Sleeping forever"
