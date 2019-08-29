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

## Interesting Commands

### Change profile (e.g. headset, a2dp) of bluetooth device

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
2. load the module by command `pactl load-module module-alsa-source device=hw:1,0` - you can also add this to `/etc/pulse/default.pa`
