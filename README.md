# Interesting Commands

## On the Client

below command will list all the loaded modules, sinks and sources

`PULSE_SERVER="tcp:localhost:4713" pactl list short`

https://github.com/mviereck/x11docker/wiki/Container-sound:-ALSA-or-Pulseaudio

`PULSE_SERVER=unix:/tmp/pulseaudio.socket pactl list short`
