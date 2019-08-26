#!/bin/bash

echo -e "STEP 1: playing LRMonoPhase4.wav"
paplay LRMonoPhase4.wav

echo -e "STEP 2: recording audio for 10 seconds "
parecord --channels=1 record_session1.wav &
sleep 10
kill $!  #$! expands to the PID of the last process executed in the background

echo -e "STEP 3: Playing recorded sample"
paplay record_session1.wav

echo -e "STEP 4: Sleeping forever"
while true; do
   # every hour a "zzz" is put into the log files.
   echo "    zzz"
   sleep 3600
done