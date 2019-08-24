#!/bin/bash

echo -e "STEP 1: playing LRMonoPhase4.wav"
paplay LRMonoPhase4.wav

echo -e "\nSTEP 2: Sleeping forever"
while true; do
   # every hour a "zzz" is put into the log files.
   echo "    zzz"
   sleep 3600
done