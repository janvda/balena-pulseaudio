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

## Configuration of the `pulseaudio-server` service

### A. Configuration of Audio devices connected via USB

If you have one or more audio devices ( speaker, camera with microphone, ...) that you want to (permanently) connect to the USB ports of the raspberry pi then they can be configured as follows:

1. Connect the audio devices to the USB ports of the raspberry pi
2. [Determine the Card ID and Device ID of all the connected audio devices](#2-determine-the-card-id-and-device-id-of-the-connected-audio-devices)
3. Set the device service variables `alsa-sink1`, `alsa-sink2`, ... , `alsa-source1`, `alsa-source2`,...
4. Validate the configuration

#### 2. Determine the Card ID and Device ID of the connected audio devices

The Card ID and Device ID of the audio devices (speaker, headset, camera with microphone, ...) that are connected to the USB ports of the raspberry py can be determined as follows:

1. Connect the audio devices to the USB ports of the raspberry pi.
2. Restart the `pulseaudio-server` service via your BalenaCloud dashboard.
3. open a terminal session for the `pulseaudio-server` service in your BalenaCloud dashboard.
4. run the command `aplay -l`.  This will list all playback devices (e.g. a speaker).  See an example output of this command below.  So you can see that besides the USB device `card 2: Device [USB2.0 Device], device 0: USB Audio [USB Audio]` it is also listing the raspberry pi audio jack (= `card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]` and the raspberry pi hdmi port (= `card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]`)

```
root@ba7c427:/# aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 7/7
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: Device [USB2.0 Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
root@ba7c427:/#
```

5. So in the above output you can easily find back the Card ID (which is 2) and the Device ID (which is 0) of the connected audio playback devices.
6. Now, we have to do the same for the audio capture devices by running the command `arecord -l`.  See an example output below which shows 2 connected audio capture devices: playstation eye camera with micro (= `card 1: CameraB409241 [USB Camera-B4.09.24.1], device 0: USB Audio [USB Audio]`) and my speaker which also has a micronphone (= `card 2: Device [USB2.0 Device], device 0: USB Audio [USB Audio]`)

```
root@ba7c427:/# arecord -l
**** List of CAPTURE Hardware Devices ****
xcb_connection_has_error() returned true
card 1: CameraB409241 [USB Camera-B4.09.24.1], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 2: Device [USB2.0 Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
root@ba7c427:/#
```

7. So in the above output you can easily find back the Card ID and Device ID of the connected audio capture devices.

#### 3. Set the device service variables `alsa_sink1`, `alsa_sink2`, ... , `alsa_source1`, `alsa-source2`,...

Setting the below device service variables for the `pulseaudio-server`service in your BalenaCloud dashboard will assure that the `pulseaudio-server` service can play or record audio from these devices.

So for each of the audio **playback** devices you want to use in pulseaudio-server you must properly set an `alsa_sink<X>` device service variable (where `<X>` should be `1` or `2` or `3`)
and for each of the audio **capture** devices you want to use you must properly set an `alsa_source<X>` device service variable.

The value of `alsa_sink<X>` must be a valid option for the pulseaudio command `load-module module-alsa-sink` and the value of `alsa_source<X>` must be a valid option for the pulseaudio command `load-module module-alsa-source`.

At least you must specify the respective playback or capture device as follows:

```
device=hw:[Card ID],[Device ID]
```

where `[Card ID]` and `[Device ID]` are respectively the Card ID and the Device ID of your connected audio device that you have identified in the previous step.

You can also specify additional options if you want.  For the possible options see

* [options for alsa_source<X> (see module-alsa-source) and alsa_sink<X> (see module-alsa-sink)](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#index4h3)
* [options supported by all device driver modules](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#index1h2)

Here below an example value for `alsa_source1`:

```
device=hw:1,0 source_name=PS3_eye_camera"
```

| Name                                            | Description |
|------------------------------------------------ | ----- |
| alsa_sink1 | specify here the Card ID and Device ID of an audio **playback** device connected to one of the USB ports of your raspberry pi. The format is `device=hw:[Card ID],[Device ID]` (E.g. `device=hw:1,0`).  You can also specify other options in this variable (see above). e.g. `device=hw:1,0 sink_name=sony_speaker` |
| alsa_sink2 | In case multiple audio **playback** devices are connected, you can use this variable for the 2nd connected playback device. |
| alsa_sink3 | Same as alsa_sink2 but for 3rd connected audio playback device. |
| alsa_source1 | specify here the Card ID and Device ID of an audio **capture** device connected to one of the USB ports of your raspberry pi. The format is `device=hw:[Card ID],[Device ID]` (E.g. `device=hw:1,0`).  You can also specify other options in this variable (see above). e.g. `device=hw:1,0 source_name=ps3_eye_camera_with_micro` |
| alsa_source2 | same as alsa_source1 but for 2nd audio capture device connected. |
| alsa_source3 | same as alsa_source1 but for 3rd audio capture device connected. |

#### 4. Validate the configuration

TBD

### B. Configuration of a Bluetooth device

If you have a bluetooth audio device (e.g. bluetooth speaker, bluetooth head-set) and you want to play and/or record audio from this device then the following is needed:

1. [Identify the device address of your bluetooth audio device](#1-identify-the-bluetooth-device-address) (e.g. `A0:E9:DB:09:CF:FF`).
2. [pair the raspberry pi with your bluetooth device](#2-pair-the-raspberry-pi-with-the-bluetooth-device)
3. [automatically connect to it by setting the device service variable `bluetooth_device_address`](#3-set-the-device-service-variable-bluetooth_device_address-for-service-pulseaudio-server)
4. [Validate the automatic connection](#4-validate-the-bluetooth-connection). (optional step)

Note that instead of step 3 you can also manually connect to the bluetooth device using the `connect <bluetooth-device-address>` command.

#### 1. Identify the bluetooth device address

There are several ways to determine the device address (a kind of MAC address) of your bluetooth device.

One possible way:

1. open a terminal session for the `pulseaudio-server` service in your BalenaCloud dashboard.
2. within that session enter the command `bluetoothctl`
3. within the `bluetoothctl`-session enter the command `scan on`.  
4. assure that your bluetooth device is switched on and listening for bluetooth connections.
5. In the `bluetoothctl`-session you should see the bluetooth device addresses appearing (e.g. `[NEW] Device 75:E0:1C:D7:D4:68 CC-RT-BLE` - where `CC-RT-BLE` is the name of the device).
6. For some bluetooth devices the scan might not display a meaningful name but the device address (e.g. `[NEW] Device 6E:F1:B6:0E:DD:51 6E-F1-B6-0E-DD-51`).  In that case [pairing with the device](#2-pair-the-raspberry-pi-with-the-bluetooth-device) might be needed first to be able to see the actual device name instead of the device address.
7. **TIP**: the command `help` will list all possible commands you can enter in the `bluetoothctl`-session.
8. the command `exit` or `quit`can be used to leave the `bluetoothctl`-session.

#### 2. Pair the raspberry pi with the bluetooth device

This should be done only once.  Once the device is paired, it is remembered even after a reboot of the raspberry pi device.

The steps for pairing:

1. open a terminal session for the `pulseaudio-server` service in your BalenaCloud dashboard.
2. within that session enter the command `bluetoothctl`
3. within the `bluetoothctl`-session enter the command `pair <bluetooth device address>`
4. With the command `info <bluetooth device address>` you can check if the pairing was successful.

 For more information about pairing: [introduction to pairing](https://docs.ubuntu.com/core/en/stacks/bluetooth/bluez/docs/reference/pairing/introduction).

#### 3. Set the device service variable `bluetooth_device_address` for service `pulseaudio-server`

If you want to automatically connect to your bluetooth audio device you have to set the following Device Service Variable for the service `pulseaudio-server` in your BalenaCloud dashboard.

| Name                                            | Description |
|------------------------------------------------ | ----- |
| **bluetooth_device_address**  | if specified then at startup, the `pulseaudio-server` will connect to this device and will retry connecting every 60 sec.  This address should have a format like `6E:F1:B6:0E:DD:51`.  Note that it will only work if [the raspberry pi has paired with this device](#2-pair-the-raspberry-pi-with-the-bluetooth-device). |

Of course it is also possible to set this environment variable in the `docker-compose.yml` for that service.

#### 4. Validate the bluetooth connection

After step 3 you can validate if an automatic connection is made to this device.

1. First assure that bluetooth audio device is able to accept bluetooth connections and is within range of your raspberry pi.
2. open a terminal session for the `pulseaudio-server` service in your BalenaCloud dashboard.
3. within that session enter the command `bluetoothctl`.  In case of successful connection you should see something like (instead of `GEAR4 SPW` you should see the name of your bluetooth device)

```
root@ba7c427:/# bluetoothctl
Agent registered
[GEAR4 SPW]#
```

4. within the `bluetoothctl`-session enter the command `info <bluetooth device address>` or most likely command `info` is sufficient.  You should get something like:

```
GEAR4 SPW]# info A0:E9:DB:09:CF:FF
Device A0:E9:DB:09:CF:FF (public)
        Name: GEAR4 SPW
        Alias: GEAR4 SPW
        Class: 0x00240404
        Icon: audio-card
        Paired: yes
        Trusted: yes
        Blocked: no
        Connected: yes
        LegacyPairing: no
        UUID: Headset                   (00001108-0000-1000-8000-00805f9b34fb)
        UUID: Audio Sink                (0000110b-0000-1000-8000-00805f9b34fb)
        UUID: Advanced Audio Distribu.. (0000110d-0000-1000-8000-00805f9b34fb)
        UUID: Handsfree                 (0000111e-0000-1000-8000-00805f9b34fb)
[GEAR4 SPW]#
```

5. Check if you see a line with `Connected: yes` in above output and this confirms that the bluetooth connection has been properly setup.

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
