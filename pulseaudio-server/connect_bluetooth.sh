#!/bin/bash
# script that connects in an endless loop to the bluetooth device with address $bluetooth_device_address

if [ "$bluetooth_device_address" != '' ]; then
   sleep 20
   echo "[$0]: Start endless loop for connecting to bluetooth device with mac = $bluetooth_device_address"
   while true; do
     bluetoothctl <<- EOF > /dev/null
        connect $bluetooth_device_address
        exit
EOF
     sleep 60
   done
fi