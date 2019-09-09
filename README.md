# balena-pulseaudio

## Introduction

This balena application runs a pulseaudio server and demonstrates how it can be used for playing and recording audio on a raspberry pi.  It also supports playing and recording audio from bluetooth audio devices (bluetooth speakers, bluetooth headsets, ...)

## Required Hardware

1. Raspberry pi (although it is most likely very easy to port this to other devices)
2. For playing audio the following can be used:
   1. headphone, earphone, ... plugged into the headphone jack of the raspberry pi.
   2. TV, monitor with speaker, ... connected to hdmi port of the raspberry pi.
   3. bluetooth speaker, bluetooth headset,...
   4. (DAC) HAT with audio device or speaker connected to it.
3. For recording audio the following can be used:
   1. USB microphone, USB camera with microphone, ...
   2. bluetooth headset, bluetooth speaker with microphone
   3. HAT with one or more microphones

## Rationale

The idea is to create a pulseaudio service (= `pulseaudio-server`) that can be reused in other balena applications requiring an audio interface.  This pulseaudio service is the only service having an interface with the audio hardware (including connected bluetooth devices): all other services requiring audio should do this via this pulseaudio service.

## Features

1. service `pulseaudio-client-tcp` demonstrates how a service can communicate with the `pulseaudio-server` via TCP.
2. service `pulseaudio-client-unix` demonstrates how a service can communicate with the `pulseaudio-server` via a unix socket.
3. demonstrate how commands `paplay`and `parecord` can be used to play and record audio.
4. Support changing/showing any pulseaudio setting through command `pactl`.
5. Support scanning/connecting/monitoring of bluetooth devices through command `bluetoothctl`
6. Supports `pavucontrol` and `audacity`.  This requires an X-server (e.g. XQuartz on macbook) that is connected to the same local network.

## Configuration

### Bluetooth device

If you want to communicate to a specific bluetooth audio device (e.g. bluetooth speaker) the following is needed:

1. [Identify the bluetooth device address](#1-identify-the-bluetooth-device-address)(e.g. `A0:E9:DB:09:CF:FF`).
2. [pair it](#2-pair-your-bluetooth-device)
3. [set the environment variable `bluetooth_device_address`](#3-set-the-environment-variable-bluetooth_device_address)

#### 1. Identify the bluetooth device address

There are several ways to determine the device address (a kind of MAC address) of your bluetooth device.

One possible way: 
1. open a terminal session for the `pulseaudio-server` service in your BalenaCloud dashboard.
2. within that session enter the command `bluetoothctl`
3. within the `bluetoothctl`-session enter the command `scan on`.  
4. assure that your bluetooth device is switched on and listening for bluetooth connections.
5. In the `bluetoothctl`-session you should see the bluetooth device addresses appearing (e.g. `[NEW] Device 75:E0:1C:D7:D4:68 CC-RT-BLE` - where `CC-RT-BLE` is the name of the device).
6. For some bluetooth devices the scan might not display a meaningful name but the device address (e.g. `[NEW] Device 6E:F1:B6:0E:DD:51 6E-F1-B6-0E-DD-51`).  In that case [pairing the device](#2-pair-your-bluetooth-device) might be needed first to be able to see the actual device name instead of the device address.
7. **TIP**: the command `help` will list all possible commands you can enter in the `bluetoothctl`-session.
7. the command `exit` or `quit`can be used to leave the `bluetoothctl`-session.


#### 2. Pair your bluetooth device

This should be done only once.  Once the device is paired, it is remembered even after a reboot of the raspberry pi device.

The steps for pairing:

1. open a terminal session for the `pulseaudio-server` service in your BalenaCloud dashboard.
2. within that session enter the command `bluetoothctl`
3. within the `bluetoothctl`-session enter the command `pair <bluetooth device address>`
4. With the command `info <bluetooth device address>` you can check if the pairing was successful.

#### 3. Set the environment variable `bluetooth_device_address`

TBD

## Interesting Commands

### Change card profile (e.g. headset, a2dp) of bluetooth device

1. Assure bluetooth device is connected (`bluetoothctl`) *TO BE DOCUMENTED*
2. Identify card number and profile names by command: `pactl list cards`
3. Change profile by command: `pactl set-card-profile <cardindex> <profilename>`.  E.g.
   1. `pactl set-card-profile 0 headset_head_unit`
   2. `pactl set-card-profile 0 a2dp_sink`

## On the Client

below commands will list all the loaded modules, sinks and sources and play an audio file

```
PULSE_SERVER="tcp:localhost:4713" pactl list short
PULSE_SERVER="tcp:localhost:4713" paplay LRMonoPhase4.wav
```

https://github.com/mviereck/x11docker/wiki/Container-sound:-ALSA-or-Pulseaudio

`PULSE_SERVER=unix:/tmp/pulseaudio.socket pactl list short`

## To add (USB) audio devices

On the server:

1. search (alsa) audio sinks using command `aplay -l` and (alsa) audio sources using command `arecord -l`
2. configure the audio source for pulseaudio by command `pactl load-module module-alsa-source device=hw:1,0` - you can also add this to `/etc/pulse/default.pa`
3. configure the audio sink for pulseaudio by command `pactl load-module module-alsa-sink device=hw:2,0` - you can also add this to `/etc/pulse/default.pa`
