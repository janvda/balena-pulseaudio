#!/bin/bash
# script that connects in an endless loop to the bluetooth device with address $bluetooth_device_address

if [ "$bluetooth_device_address" != '' ]; then
   echo "start endless loop for connecting to bluetooth device with mac = $bluetooth_device_address"
   while (sleep 30)
   do
      bluetoothctl <<- EOF > /dev/null
         connect $bluetooth_device_address
         exit
      EOF
   done
fi