# Interesting Commands

1. activate 

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
