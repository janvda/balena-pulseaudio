#!/bin/bash

# export bluetooth_device_address="A0:E9:DB:09:CF:FF"

if [ "$bluetooth_device_address" != '' ]; then
   echo "sleeping 40 sec..."
   sleep 20
   echo "connecting to bluetooth device with mac = $bluetooth_device_address"
   echo -e 'connect $bluetooth_device_address' | bluetoothctl
   sleep 20
   echo -e 'info $bluetooth_device_address' | bluetoothctl
   #echo -e 'disconnect $bluetooth_device_address' | bluetoothctl
   echo "end of connecting"
fi

echo starting pulseaudio ...
pulseaudio --log-level=4
echo ERROR: pulseaudio stopped
