# Service `pulseaudio-rest-api`

This service provides a REST HTTP interface to control the pulseaudio server.  So, other applications can send commands (via sending appropriate http request) to this service in order to control the audio volume, mute/unmute the audio, get information about connected audio devices, ...

The idea is to provide same functionality as [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/)

## Design

This service is realized by the python program ["app.py"](app.py) which uses the following python libraries:

* [flask](https://flask.palletsprojects.com/en/1.1.x/) for handling the http requests
* [pulsectl](https://pypi.org/project/pulsectl/) for communication with a pulseaudio server.
* [jsonpickle](https://jsonpickle.github.io/) to convert python objects into JSON.

Note that the home location (e.g. [http://127.0.0.1:5000/](http://127.0.0.1:5000/) ) provided by the "app.py" python program is returning an html page documenting all the methods implemented by the pulsectl library.  So this page helped me identifying the actual pulsectl methods I can use to implement this API.

## HTTP Interface

The responses will have similar structure as the data structures documented at [PulseAudio 13.0](https://freedesktop.org/software/pulseaudio/doxygen/annotated.html)

The supported command/queries are a subset of what is documented at  [PulseAudio 13.0 - Server Query and Control](https://freedesktop.org/software/pulseaudio/doxygen/introspect.html)

| URL | method | Description |
|--------|-------------|----|
| `/`| GET | returns `pulsectl` documentation of all python methods in html format |
| `/server_info`| GET | returns a `server_info` object in json format.|
| `/sink_list`| GET | returns an array of `sink_info` objects in json format.|
| `/source_list`| GET | returns an array of `source_info` objects in json format.|
| `/sink_input_list`| GET | returns an array of `sink_input_info` objects in json format.|
| `/source_input_list`| GET | returns an array of `source_input_info` objects in json format.|
| `/card_list`| GET | returns an array of `card_info` objects in json format.|
| `/card_profile_set_by_index`| PUT | input is JSON with structure { "index" : `index_of_card`, "name" : `profile_name` }.  So this request changes the profile of the card with index = `index_of_card` to the profile with name = `profile_name`. |
| `/default_sink_index`| GET, PUT | `GET` : get the index of the default sink; `PUT`: changes the default sink to the sink with the specified index. |
| `/default_source_index`| GET, PUT | similar as `/default_sink_index` |
| `/default_sink_volume`| GET, PUT | `GET`: get the volume (a number between 0 and 2, 1 stands for 100%) of the default sink; `PUT`: sets the volume of the default sink to the volume specified. |
| `/default_source_volume`| GET, PUT | similar as `/default_sink_volume` |

changes the card profile of the card with `source_input_info` objects in json format.|

| `get_card_list`| |

| `set_(sink|source)_volume_by_index` | to be implemented|
| `set_(sink|source)_mute_by_index` | to be implemented|
| `set_(sink_input|source_output)_volume` | to be implemented |
