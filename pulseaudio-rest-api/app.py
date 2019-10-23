# inspired by https://kite.com/blog/python/flask-restful-api-tutorial/
from flask import Flask, request
import pulsectl, os, time
import jsonpickle
import pydoc

app = Flask(__name__)

# Prepare session with pulseaudio server
pulse = pulsectl.Pulse('pulseaudio-rest-api', connect=False, threading_lock=True)

def pulseConnectIfNeeded():
  # This method must be called in every flask route function as this
  # will assure that it will reconnect to the pulseaudio server
  # if needed.
  if (not pulse.connected):
    pulse.connect()

try:
  pulseConnectIfNeeded()
except pulsectl.PulseError as error:
  print(error)

@app.route('/')
def help():
    pulseHelpHtml=pydoc.render_doc(pulse,renderer=pydoc.HTMLDoc())
    return pulseHelpHtml


@app.route('/server_info')
def getServerInfo():
  pulseConnectIfNeeded()
  pulsectlObject=pulse.server_info()
  return jsonpickle.encode(pulsectlObject)

@app.route('/card_list')
def getCardInfo():
  pulseConnectIfNeeded()
  pulsectlObject=pulse.card_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/sink_list')
def getSinkList():
  pulseConnectIfNeeded()
  pulsectlObject=pulse.sink_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/source_list')
def getSourceList():
  pulseConnectIfNeeded()
  pulsectlObject=pulse.source_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/sink_input_list')
def getSinkInputList():
  pulseConnectIfNeeded()
  pulsectlObject=pulse.sink_input_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/source_output_list')
def getSourceOutputList():
  pulseConnectIfNeeded()
  pulsectlObject=pulse.source_output_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/default_sink_index', methods=['GET', 'PUT'])
def DefaultSinkIndex():
  pulseConnectIfNeeded()
  if request.method == 'GET':
    try:
      defaultSinkName=pulse.server_info().default_sink_name
      print(defaultSinkName)
      indexes=[x.index for x in pulse.sink_list() if x.name == defaultSinkName] 
      print(indexes)
      assert(len(indexes)>0),"No sink found with default_sink_name - bug in pulsectl ?"
      return str(indexes[0])
    except AssertionError as error:
      return str(error), 500
    except:
      return "Unknow Error",500
  if request.method == 'PUT':
    try:
      NewDefaultSinkIndex = int(request.data) # read index from body (=msg.payload in node-red)
      sinks=[x for x in pulse.sink_list() if x.index == NewDefaultSinkIndex ]
      assert(len(sinks)!=0), "No sink found with index = " + str(NewDefaultSinkIndex)
      assert(len(sinks)==1), "Multiple sinks found with index = " + str(NewDefaultSinkIndex)
      pulse.sink_default_set(sinks[0])
      return str(NewDefaultSinkIndex)
    except AssertionError as error:
      return str(error), 400
    except:
      return "Unknow Error",400

@app.route('/default_source_index', methods=['GET', 'PUT'])
def DefaultSourceIndex():
  pulseConnectIfNeeded()
  if request.method == 'GET':
    try:
      defaultSourceName=pulse.server_info().default_source_name
      print(defaultSourceName)
      indexes=[x.index for x in pulse.source_list() if x.name == defaultSourceName] 
      print(indexes)
      assert(len(indexes)>0),"No source found with default_source_name - bug in pulsectl ?"
      return str(indexes[0])
    except AssertionError as error:
      return str(error), 500
    except:
      return "Unknow Error",500
  if request.method == 'PUT':
    try:
      NewDefaultSourceIndex = int(request.data) # read index from body (=msg.payload in node-red)
      sources=[x for x in pulse.source_list() if x.index == NewDefaultSourceIndex ]
      assert(len(sources)!=0), "No source found with index = " + str(NewDefaultSourceIndex)
      assert(len(sources)==1), "Multiple sinks found with index = " + str(NewDefaultSourceIndex)
      pulse.source_default_set(sources[0])
      return str(NewDefaultSourceIndex)
    except AssertionError as error:
      return str(error), 400
    except:
      return "Unknow Error",400

@app.route('/default_sink_volume', methods=['GET', 'PUT'])
def DefaultSinkVolume():
  pulseConnectIfNeeded()
  if request.method == 'GET':
    defaultSinkVolume=pulse.volume_get_all_chans(pulse.get_sink_by_name(pulse.server_info().default_sink_name))
    return jsonpickle.encode(defaultSinkVolume)
  if request.method == 'PUT':
    try:
      newVolume = float(request.data) # read volume from body (msg.payload in node-red)
      assert(newVolume>=0 and newVolume <= 2), "Volume [=" + str(newVolume) +  "] must be between 0 and 2"
      # TBD add interval checking
      x=pulse.volume_set_all_chans(pulse.get_sink_by_name(pulse.server_info().default_sink_name), newVolume)
      return jsonpickle.encode(newVolume)
    except ValueError:
      return "not a float", 400
    except AssertionError as error:
      return str(error), 400

@app.route('/default_source_volume', methods=['GET', 'PUT'])
def DefaultSourceVolume():
  pulseConnectIfNeeded()
  if request.method == 'GET':
    defaultSourceVolume=pulse.volume_get_all_chans(pulse.get_source_by_name(pulse.server_info().default_source_name))
    return jsonpickle.encode(defaultSourceVolume)
  if request.method == 'PUT':
    try:
      newVolume = float(request.data) # read volume from body (msg.payload in node-red)
      assert(newVolume>=0 and newVolume <= 2), "Volume [=" + str(newVolume) +  "] must be between 0 and 2"
      # TBD add interval checking
      x=pulse.volume_set_all_chans(pulse.get_source_by_name(pulse.server_info().default_source_name), newVolume)
      return jsonpickle.encode(newVolume)
    except ValueError:
      return "not a float", 400
    except AssertionError as error:
      return str(error), 400

@app.route('/default_sink_mute', methods=['GET', 'PUT'])
def DefaultSinkMute():
  pulseConnectIfNeeded()
  if request.method == 'GET':
    defaultSinkMute=pulse.get_sink_by_name(pulse.server_info().default_sink_name).mute
    return str(defaultSinkMute)
  if request.method == 'PUT':
    try:
      newMute = int(request.data) # read volume from body (msg.payload in node-red)
      assert(newMute ==0 or newMute==1), "Mute [=" + str(newMute) +  "] must be 0 (=not muted) or 1 (=muted)."
      # TBD add interval checking
      x=pulse.sink_mute(pulse.get_sink_by_name(pulse.server_info().default_sink_name).index,newMute)
      return str(newMute)
    except ValueError:
      return "not an int", 400
    except AssertionError as error:
      return str(error), 400

@app.route('/default_source_mute', methods=['GET', 'PUT'])
def DefaultSourceMute():
  pulseConnectIfNeeded()
  if request.method == 'GET':
    defaultSourceMute=pulse.get_source_by_name(pulse.server_info().default_source_name).mute
    return str(defaultSourceMute)
  if request.method == 'PUT':
    try:
      newMute = int(request.data) # read volume from body (msg.payload in node-red)
      assert(newMute ==0 or newMute==1), "Mute [=" + str(newMute) +  "] must be 0 (=not muted) or 1 (=muted)."
      # TBD add interval checking
      x=pulse.source_mute(pulse.get_source_by_name(pulse.server_info().default_source_name).index,newMute)
      return str(newMute)
    except ValueError:
      return "not an int", 400
    except AssertionError as error:
      return str(error), 400

# expects a json body as input with following 2 fields { "index" : <card index> , "name" : <profile name> }
@app.route('/card_profile_set_by_index', methods=['PUT'])
def CardProfileSetByIndex():
  pulseConnectIfNeeded()
  if request.method == 'PUT':
    try:
      content = request.get_json()
      #print(content)
      index = int(content['index'])
      name = content['name']
      assert(name != ''), "profile name not specified or blank"
      x=pulse.card_profile_set_by_index(index,name)
      return "OK"
    except TypeError as error:
      return "TypeError (input is not of type json):" + str(error), 400
    except pulsectl.PulseOperationFailed as error:
      return "pulsectl.PulseOperationFailed (name and/or index are not correct):" + str(error), 404
    except KeyError as error:
      return "keyError: json input is expected with key:" + str(error), 400
    except IndexError as error:
      return "IndexError: " + str(error), 400
    except ValueError:
      return "index not specified or not an int", 400
    except AssertionError as error:
      return str(error), 400

# expects a json body as input with following 3 fields 
#      { 
#        "source"     : <index or name of source, if not specified then default source is used > , 
#        "timeout"    : <duration in sec - e.g. 0.8 >, 
#        "stream_idx" : <optional, if specified monitors the stream with this index linked to the source>
#      }
@app.route('/get_peak_sample')
def GetPeakSample():
  pulseConnectIfNeeded()
  try:
    content = request.get_json()
    print(content)
    source  = content['index']
    timeout = content['timeout']
    assert( timeout is not None ), "timeout must be specified"
    assert( isinstance(timeout, (int,float))), "timeout must be float"
    stream_idx = content['stream_idx']
    assert( (stream_idx is None) or (isinstance(stream_idx, int))), "If stream_idx is specified then it must be a number"
    peak_volume = pulse.get_peak_sample(source,timeout,stream_idx)
    return str(peak_volume)
  except TypeError as error:
    return "TypeError (input is not of type json):" + str(error), 400
  except pulsectl.PulseOperationFailed as error:
    return "pulsectl.PulseOperationFailed (name and/or index are not correct):" + str(error), 400
  except KeyError as error:
    return "keyError: json input is expected with key:" + str(error), 400
  except IndexError as error:
    return "IndexError: " + str(error), 400
  except ValueError:
    return "index not specified or not an int", 400
  except AssertionError as error:
    return str(error), 400


# TO BE DELETED HERE BELOW
#@app.route('/sink_volume_set/<index>', methods=['POST'])
#def getSinkVolumeSet(index):
#  sink=pulse.sink_list()[int(index)]
#  return "TO BE IMPLEMENTED"
