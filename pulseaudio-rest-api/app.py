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

@app.route('/sink_volume_set/<index>', methods=['POST'])
def getSinkVolumeSet(index):
  volume = request.data # read volume from body (msg.payload in node-red)
  sink=pulse.sink_list()[int(index)]
  return jsonpickle.encode(sink)
