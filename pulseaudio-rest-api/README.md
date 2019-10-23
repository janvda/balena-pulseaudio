# Service pulseaudio-rest-api

This service provides a REST HTTP interface to control the pulseaudio server.  So, other applications can send commands (via sending appropriate http request) to this service in order to control the audio volume, get the list of sinks (audio playback devices) and sources (audio capture devices), ... of the audio devices controlled by the pulseaudio server.

The idea is to provide same functionality as [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/)

## Design

This service is realized by the python program ["app.py"](app.py) which is based on: 
* [flask](https://flask.palletsprojects.com/en/1.1.x/) library to handle the http requests
* [pulsectl](https://pypi.org/project/pulsectl/) library to communicate with a pulseaudio server

## Interface

The responses will have similar structure as the data structures documented at [PulseAudio 13.0](https://freedesktop.org/software/pulseaudio/doxygen/annotated.html)

The supported command/queries are a subset of what is documented at  [PulseAudio 13.0 - Server Query and Control](https://freedesktop.org/software/pulseaudio/doxygen/introspect.html)

| method | response |
|--------|-------------|
| `get_server_info`| returns `server_info` (includes name of default sink/source) |
| `get_card_list`| |
| `get_(sink|source)_info_list` | returns an array of `(sink|source)_info` |
| `get_(sink_input|soure_output)_info_list` | returns an array of  `(sink_input|source_output)_info`|
| `set_(sink|source)_volume_by_index` | to be implemented|
| `set_(sink|source)_mute_by_index` | to be implemented|
| `set_(sink_input|source_output)_volume` | to be implemented |


