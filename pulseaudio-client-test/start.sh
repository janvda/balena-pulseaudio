#!/bin/bash

cd /data

# see https://github.com/janvda/balena-pulseaudio/issues/13
unset DISPLAY

echo "Listing all cards (=bluetooth):"
pactl list cards | grep "Card\|Name\|description\|Active Profile"

if [ "$card_profile" != "" ]; then
   if [ "$card_index" = "" ]; then
      card_index=0
   fi
   echo "Set card profile of card $card_index to $card_profile "
   pactl set-card-profile $card_index $card_profile
fi

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

# set default recording time to 10 sec.
if [ "$recording_time" = "" ]; then
   recording_time=10  
fi

echo "Listing default sink and source:"
pactl info | grep "Sink\|Source"

case $test_id in
"") echo "INFO: You can specify a specific test by setting \$test_id."
   ;;
0) ;;
1) echo "Starting test 1 - play audio file using paplay :"
   paplay LRMonoPhase4.wav
   echo "... end of test 1"
   ;;
2) echo "Starting test 2: "
   echo "- Starting recording audio within 5 sec !"
   paplay ./test_id_2/step1_welcome.wav
   sleep 3
   echo "- Recording for $recording_time seconds started ... (SAY SOMETHING) "
   paplay ./test_id_2/step2_recording_starts.wav
   parecord --channels=1 record_session1.wav &
   sleep $recording_time
   kill $! #$! expands to the PID of the last process executed in the background
   echo "- Recording finished !"
   paplay ./test_id_2/step3_recording_finished.wav
   sleep 2
   paplay ./test_id_2/step4_play_recording.wav
   echo "- Playing recorded audio..."
   paplay record_session1.wav
   echo "... end of test 2"
   paplay ./test_id_2/step5_end_of_playing.wav
   ;;
3) if [ "$remote_display" = "" ]; then
     echo "ERROR: \$remote_display must be set for test 3 and is not set !"
   else
     echo "launching pavucontrol ..."
     DISPLAY=$remote_display pavucontrol 
   fi
   ;;
4) if [ "$remote_display" = "" ]; then
     echo "ERROR: \$remote_display must be set for test 4 and is not set !"
   else
     echo "launching audacity ..."
     DISPLAY=$remote_display audacity
   fi
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
