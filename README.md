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

## Services
This balena application consists of following services:

* `pulseaudio-server` : the core service running the pulseaudio server.  For its documentation and configuration see its [README](pulseaudio-server/README.md)
* `pulseaudio-client-tcp` and `pulseaudio-client-unix` are 2 test services based on the same docker container `pulseaudio-client-test`. For its documentation and configuration see its [README](pulseaudio-client-test/README.md) !!


## Running `pavucontrol` or `audacity` so that its UI (user interface) is displayed on macbook.

pavucontrol and audacity are both X11 applications.  The following steps describe how to run these X11 applications in one of the pulseaudio services (e.g. `pulseaudio-client-unix` service) and get its UI (user interface) displayed on a macbook connected to the same LAN:

1. On your macbook run X-windows and authorize raspberry pi as specified by below steps:
    1. Assure that your macbook is connected to the same LAN.
    2. Install [XQuartz v2.7.11](https://www.xquartz.org) (= X Window System) on your macbook.
    3. Update firewall rules (under `System Preferences`> `Security & Privacy` > `Firewall Options ...`) so that it is allowing incoming connections for the `XQuartz` application.
    4. Launch XQuartz and in its settings: go to Security tab and enable `Authenticate connections` and Àllow connections from network clients`
    5. open an xterm window (this can be done via XQuartz menu: applications > terminal)
    6. within xterm window enter the commands `xhost +<ip address raspberry pi>` (The `<ip address raspberry pi>` can be found in the BalenaCloud dashboard).  This allows the raspberry pi to display on the XQuartz window system.  Note if the raspberry pi has 2 IP addresses (Wi-Fi and Ethernet) then enter the `xhost +` for both IP addresses.
    7. Validate the authorizations set in previous step by running command `xhost`.  You should see something like:

```
bash-3.2$ xhost
access control enabled, only authorized clients can connect
INET:ba7c427.lan
INET:192.168.1.58
bash-3.2$ 
```

2. Determine the Wi-Fi IP address of your macbook as specified by below steps:
   1. on your macbook: go to system preferences > network. 
   2. Select Wi-Fi > Advanced...
   3. select TCP/IP and the displayed `ÌPv4 Address` is the IP Address we need.
   4. Note that it is also possible to determine this IP address by running the command `ìfconfig` in a terminal window.
3. Launch pavucontrol or audacity on the raspberry pi as specified by below steps:
   1. Within your BalenaCloud dashboard open a terminal window for the `pulseaudio-server` or `pulseaudio-client-{tcp|unix}`service.
   2. In case you want to run pavucontrol:
       1. In the terminal window: enter the command `DISPLAY=<ip address of macbook>:0 pavucontrol` (e.g. `DISPLAY=192.168.1.5:0 pavucontrol`) where `<ip address of macbook>`is the IP address determined in previous step.
       2. you should now see the `pavucontrol` UI (user interface) appearing on your macbook.
   3. In case you want to run audacity:
       1. In the terminal window: Enter the command `DISPLAY=<ip address of macbook>:0 audacity` (e.g. `DISPLAY=192.168.1.5:0 audacity`)
       2. you should now see the `audacity` UI (user interface) appearing on your macbook.

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
