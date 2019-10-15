# inspired by https://kite.com/blog/python/flask-restful-api-tutorial/
from flask import Flask, request
import pulsectl, os, time
import jsonpickle
import pydoc

app = Flask(__name__)

# Connect to pulseaudio server
pulse = pulsectl.Pulse('pulseaudio2mqtt')

@app.route('/')
def help():
    pulseHelpHtml=pydoc.render_doc(pulse,renderer=pydoc.HTMLDoc())
    return pulseHelpHtml

@app.route('/server_info')
def getServerInfo():
  pulsectlObject=pulse.server_info()
  return jsonpickle.encode(pulsectlObject)

@app.route('/card_list')
def getCardInfo():
  pulsectlObject=pulse.card_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/sink_list')
def getSinkList():
  pulsectlObject=pulse.sink_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/source_list')
def getSourceList():
  pulsectlObject=pulse.source_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/sink_input_list')
def getSinkInputList():
  pulsectlObject=pulse.sink_input_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/source_output_list')
def getSourceOutputList():
  pulsectlObject=pulse.source_output_list()
  return jsonpickle.encode(pulsectlObject)

@app.route('/default_sink_index', methods=['GET', 'PUT'])
def DefaultSinkIndex():
  if request.method == 'GET':
    try:
      defaultSinkName=pulse.server_info().default_sink_name
      print(defaultSinkName)
      indexes=[x.index for x in pulse.sink_list() if x.name == defaultSinkName]  # list of all elements with .n==30
      print(indexes)
      assert(len(indexes)>0),"No sink found with default_sink_name - bug in pulsectl ?"
      return str(indexes[0])
    except AssertionError as error:
      return str(error), 500
    except:
      return "Unknow Error",500
  if request.method == 'PUT':
    try:
      NewDefaultSinkIndex = int(request.data) # read volume from body (msg.payload in node-red)
      # next functin is not correct as it is expecting the index.
      sinks=[x for x in pulse.sink_list() if x.index == NewDefaultSinkIndex ]
      assert(len(sinks)!=0), "No sink found with index = " + str(NewDefaultSinkIndex)
      assert(len(sinks)==1), "Multiple sinks found with index = " + str(NewDefaultSinkIndex)
      pulse.sink_default_set(sinks[0])
      return str(NewDefaultSinkIndex)
    except AssertionError as error:
      return str(error), 400
    except:
      return "Unknow Error",400

@app.route('/default_sink_volume', methods=['GET', 'PUT'])
def DefaultSinkVolume():
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


# TO BE DELETED HERE BELOW
#@app.route('/sink_volume_set/<index>', methods=['POST'])
#def getSinkVolumeSet(index):
#  sink=pulse.sink_list()[int(index)]
#  return "TO BE IMPLEMENTED"
