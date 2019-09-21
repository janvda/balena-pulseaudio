# Test services: `pulseaudio-client-tcp` and `pulseaudio-client-unix`

`pulseaudio-client-tcp` and `pulseaudio-client-unix` are both based on the same docker container = `pulseaudio-client-test`.
The only difference is how they communicate with the pulseaudio server:

* `pulseaudio-client-tcp` uses a TCP socket.
* `pulseaudio-client-unix` uses unix socket.

These services allow to test and demonstrate the functionality provided by service `pulseaudio-server`.  This can be done by properly setting device service variables. The core of this logic is encoded in the [start.sh](start.sh) script.

## Device Service Variables

| Name                                            | Description |
|------------------------------------------------ | ----- |
| PULSE_SERVER | Normally You should not set this variable.  It is set in the docker-compose.yml file as follows `PULSE_SERVER=tcp:localhost:4713` for `pulseaudio-client-tcp` and `PULSE_SERVER=unix:/pulseaudio/unix_socket` for `pulseaudio-client-unix`. |
| test_id | specifies the test scenario to run (see below) |
| card_profile | if specified then the connected bluetooth device with index = `$card_index` will be set to this profile.  Typical values are `a2dp_sink`, `headset_head_unit`and `off` |
| card_index | default value is `0`. For its meaning see description `card_profile`|
| default_sink | Specifies which sink (playback device) to use as default sink.  You can specify it by its index or name. |
| default_source | Specifies which source (audio capture device) to use as default source.  You can specify it by its index or name. |
| recording_time | Specifies how long (in seconds) to record audio.  This is only applicable in case recording is part of the test scenario. |
| remote_display | defines the remote display for X-appliations. E.g. `remote_display=192.168.1.5:0` |
| smbd | if set to `1` then this assures that the samba deamon is running which will make the folder (= `\data`) containing the (recorded) audio files accessible as a windows share at `smb:\\<IP address raspberry pi>\data` for `guest` user.  In order to get no conflicts, do NOT set this for both services.|

### Test scenarios

We can run a specific scenario by setting the device service variable `test_id`.

| test_id                                   | Description |
|------------------------------------------ | ----- |
| 0 | No test run |
| 1 | play a sample audio file |
| 2 | record audio for short period + play recorded audio |
| 3 | launches [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/).  Requires that variable `remote_display` is properly. |
| 4 | launches [audacity](https://www.audacityteam.org/). Requires that variable `remote_display` is properly. Note that audacity is working but due to the remote X server setup the audacity user interface is not very responsive. |

[back to main README](../README.md)
