# Service pulseaudio2mqtt

This service provides an MQTT interface to a pulseaudio server.  So, other applications can send commands (via publishing appropriate MQTT messages) to this service to control the audio volume, list the sinks (audio playback devices), list the sources (audio capture devices), ... of the audio devices controlled by the pulseaudio server.

The idea is to provide same functionality over MQTT as [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/) (excluding the real time volume monitoring).

## Interface

The MQTT responses will have similar structure as the data structures documented at [PulseAudio 13.0](https://freedesktop.org/software/pulseaudio/doxygen/annotated.html)

The supported command/queries are a subset of what is documented at:
* [PulseAudio 13.0 - Server Query and Control](https://freedesktop.org/software/pulseaudio/doxygen/introspect.html)

| method | Description |
|--------|-------------|
| `get_(sink|source)_info_list` | returns an array of `(sink|source)_info` |
| `get_(sink_input|soure_output)_info_list` | returns an array of  `(sink_input|source_output)_info`|
| `set_(sink|source)_volume_by_index` | |
| `set_(sink|source)_mute_by_index` | |
| `set_(sink_input|source_output)_volume` ||


## Design

This service is a python program that uses 
* the [pulsectl](https://pypi.org/project/pulsectl/) library to communicate with a pulseaudio server
* the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library to implement the mqtt interface.
