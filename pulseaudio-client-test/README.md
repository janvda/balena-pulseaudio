# Test Services: `pulseaudio-client-tcp` and `pulseaudio-client-unix`

`pulseaudio-client-tcp` and `pulseaudio-client-unix` are both based on the same docker container = `pulseaudio-client-test`.
The only difference is how they communicate with the pulseaudio server:

* `pulseaudio-client-tcp` use TCP sockets
* `pulseaudio-client-unix` uses unix sockets.

These services allow to test and demonstrate the funtionality provided by service `pulseaudio-server`.  This can be done by properly setting device service variables. The core of this logic is encoded in the [start.sh](start.sh) script.

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

### Test scenarios

We can run a specific scenario by setting the device service variable

| test_id                                   | Description |
|------------------------------------------ | ----- |
| 0 | No test run |
| 1 | play a sample audio file |
| 2 | record audio for short period + play recorded audio |
| 3 | NOT YET IMPLEMENTED. launches pavucontrol.  Requires `$remote_display` being set properly.
| 4 | NOT YET IMPLEMENTED. launches audacity. Requires `$remote_display` being set properly.|
