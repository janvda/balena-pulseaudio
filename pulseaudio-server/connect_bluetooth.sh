#!/bin/bash

# export bluetooth_device_address="A0:E9:DB:09:CF:FF"

if [ "$bluetooth_device_address" != '' ]; then
   echo "start connection loop for bluetooth device with mac = $bluetooth_device_address"
   while (sleep 30)
   echo "  reconnecting to $bluetooth_device_address if needed ..."
   do
bluetoothctl << EOF
connect $bluetooth_device_address
exit
EOF
   done

   #echo -e 'connect $bluetooth_device_address' | bluetoothctl
   #echo -e 'info $bluetooth_device_address' | bluetoothctl
   #echo -e 'disconnect $bluetooth_device_address' | bluetoothctl
   echo "end of connecting"
fi