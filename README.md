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

The idea is to create a pulseaudio service (= `pulseaudio-server`) and a REST interface (= `pulseaudio-rest-api` service) for audio control (_e.g. setting volume, mute, unmute, specify default sink (audio playback device) or sink (audio capture device), ..._) that can be reused in other balena applications requiring an audio interface.  The pulseaudio service is the only service having an interface with the audio hardware (_includes connected bluetooth devices_): all other services requiring audio should communicate with the pulseaudio service AND use the REST interface for controlling the audio.

## Features

1. service `pulseaudio-client-tcp` demonstrates how a service can communicate with the `pulseaudio-server` via TCP.
2. service `pulseaudio-client-unix` demonstrates how a service can communicate with the `pulseaudio-server` via a unix socket.
3. demonstrate how commands `paplay`and `parecord` can be used to play and record audio.
4. Support changing/showing any pulseaudio setting through command `pactl`.
5. Support scanning/connecting/monitoring of bluetooth devices through command `bluetoothctl`
6. Supports `pavucontrol` and `audacity`.  This requires an X-server (e.g. XQuartz on macbook) that is connected to the same local network.

## Services
This balena application consists of following services:

1. `pulseaudio-server` : the core service running the pulseaudio server.  
   * For its documentation and configuration see [pulseaudio-server/README.md](pulseaudio-server/README.md)
2. `pulseaudio-rest-api`: provides a REST API for controlling the `pulseaudio-server`.
   * For its documentation and configuration see [pulseaudio-rest-api/README.md](pulseaudio-rest-api/README.md)
3. `pulseaudio-client-tcp` and `pulseaudio-client-unix` are 2 test services based on the same docker container `pulseaudio-client-test`. 
   * For its documentation and configuration see [pulseaudio-client-test/README.md](pulseaudio-client-test/README.md)
4. `node-red`: demonstrates how the REST api (`pulseaudio-rest-api) can be used in node-red to control the `pulseaudio-server`
5. `samba`: Gives access (as windows share) to the `\data` folder of the `node-red` service and the `pulseaudio-client-unix` service (see [docker-compose.yml](./docker-compose.yml))
