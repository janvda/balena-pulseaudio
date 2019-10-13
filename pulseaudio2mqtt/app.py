# inspired by https://kite.com/blog/python/flask-restful-api-tutorial/
from flask import Flask, request
import pulsectl, json, os, time
import jsonpickle

app = Flask(__name__)

# Connect to pulseaudio server
pulse = pulsectl.Pulse('pulseaudio2mqtt')

class PulseAudioJSONEncorder(json.JSONEncoder):
    def default(self,obj):
        if ( type(obj) == pulsectl.pulsectl.PulseServerInfo) :
            return PulseAudioJSONEncorder.default(self,   
                             { "user_name": 10,
                               "host_name": "ikke" } )
        return json.JSONEncoder.default(self, obj)

@app.route('/')
def index():
    return 'Index Page'

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