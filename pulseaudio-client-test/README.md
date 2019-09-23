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
| 3 | launches [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/).  Requires that variable `remote_display` is properly set. For display on macbook read [section below](README.md#running-pavucontrol-or-audacity-so-that-its-ui-user-interface-is-displayed-on-macbook).|
| 4 | launches [audacity](https://www.audacityteam.org/). Requires that variable `remote_display` is properly set.  For display on macbook read [section below](README.md#running-pavucontrol-or-audacity-so-that-its-ui-user-interface-is-displayed-on-macbook).  Note that audacity is working but due to the remote X server setup the audacity user interface is not very responsive. |

## Manually changing card profile of a connected bluetooth device

Bluetooth audio devices might support multiple card profiles.  Typically there are 3 profiles:
* `a2dp_sink`
* `headset_head_unit`
* `off`

Instead of using the device service variable (`card_profile`and `card_index`) you can also manually set the card profile by executing the following commands in a terminal window for this service in the balenaCloud dashboard:
1. Assure that the bluetooth device is connected to the pulseaudio-server.
2. Identify card number and profile names by command: `pactl list cards`
2. Change profile by command: `pactl set-card-profile <cardindex> <profilename>`. E.g.
   * `pactl set-card-profile 0 headset_head_unit`
   * `pactl set-card-profile 0 a2dp_sink`

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
3. Set device service variable `remote_display=<ip address found in previous step>:0` (e.g. `192.168.1.5:0`) and `test_id=3` for service `pulseaudio-client-tcp` or `pulseaudio-client-unix`.  This will make that pavucontrol is automatically launched at startup by the server.  If you want to launch audacity at startup you have to set the `test_id=4`.
4. Instead of step 3 you can of course also manually launch pavucontrol or audacity on the raspberry pi as specified by below steps:
   1. Within your BalenaCloud dashboard open a terminal window for the `pulseaudio-server` or `pulseaudio-client-{tcp|unix}`service.
   2. In case you want to run pavucontrol:
       1. In the terminal window: enter the command `DISPLAY=<ip address of macbook>:0 pavucontrol` (e.g. `DISPLAY=192.168.1.5:0 pavucontrol`) where `<ip address of macbook>`is the IP address determined in previous step.
       2. you should now see the `pavucontrol` UI (user interface) appearing on your macbook.
   3. In case you want to run audacity:
       1. In the terminal window: Enter the command `DISPLAY=<ip address of macbook>:0 audacity` (e.g. `DISPLAY=192.168.1.5:0 audacity`)
       2. you should now see the `audacity` UI (user interface) appearing on your macbook.

[back to main README](../README.md)
