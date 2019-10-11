import pulsectl, json, os, time
import paho.mqtt.client as mqtt
from datetime import datetime

############## FUNCTION TO CONVERT the PULSECTL OBJECTS INTO JSON strings #################
def unsupported_type2json(obj):
   return '{ "UNSUPPORTED TYPE - ' + str(type(obj)) + '" : "obj=' + str(obj) + '"}'

def list2json(obj):
   json_str="["
   first= True
   for i in obj:
      if first :
         first= False
      else:
         json_str += ","
      json_str += object2json(i)
   json_str += "]"
   return json_str

def dict2json(obj):
   # replade single quote by double quotes
   return str(obj).replace("'",'"')

def server_info2json(obj):
   json_str = '{ "server_info" : { "user_name":"'       + obj.user_name       + '",'  + \
                                 '"host_name":"'        + obj.host_name       + '",'  + \
                                 '"server_version":"'   + obj.server_version  + '",'  + \
                                 '"server_name":"'      + obj.server_name     + '",'  + \
                                 '"default_sink_name":"'   + obj.default_sink_name    + '",'  + \
                                 '"default_source_name":"' + obj.default_source_name  + '",'  + \
                                 '"cookie":'      + str(obj.cookie) + '}}'
   return json_str

def card_info2json(obj):
   json_str = '{ "card_info" : { "index":'              + str(obj.index)         + ','  + \
                                 '"name":"'             + obj.name               + '",' + \
                                 '"owner_module":'      + str(obj.owner_module)  + ','  + \
                                 '"driver":"'           + obj.driver             + '",' + \
                                 '"n_profiles":'       + str(obj.n_profiles)    + ','  + \
                                 '"profile_active":'   + object2json(obj.profile_active) + ','  + \
                                 '"profile_list":'     + object2json(obj.profile_list) + ','  + \
                                 '"propplist":'        + object2json(obj.proplist)   + '}}'
   return json_str

def card_profile_info2json(obj):
   json_str = '{ "card_profile_info" : { "name":"'    + obj.name           + '",' + \
                                 '"description":"'    + obj.description    + '",' + \
                                 '"n_sinks":'         + str(obj.n_sinks)   + ','  + \
                                 '"n_sources":'       + str(obj.n_sources) + ','  + \
                                 '"priority":'        + str(obj.priority)  + ','  + \
                                 '"available":'       + str(obj.available) + '}}'
   return json_str

def sink_info2json(obj):
   json_str = '{ "sink_info" : { "index":'        + str(obj.index)  + ','   + \
                                 '"description":"'+ obj.description + '",'  + \
                                 '"name":"'       + obj.name        + '",'  + \
                                 '"mute":'        + str(obj.mute)   + ','   + \
                                 '"proplist":'     + object2json(obj.proplist)  + ','  + \
                                 '"cvolume":'      + object2json(obj.volume) + '}}'
   return json_str

def source_info2json(obj):
   json_str = '{ "source_info" : { "index":'        + str(obj.index)  + ','   + \
                                 '"description":"'+ obj.description + '",'  + \
                                 '"name":"'       + obj.name        + '",'  + \
                                 '"mute":'        + str(obj.mute)   + ','   + \
                                 '"proplist":'     + object2json(obj.proplist)  + ','  + \
                                 '"cvolume":'      + object2json(obj.volume) + '}}'
   return json_str

def sink_input_info2json(obj):
   json_str = '{ "sink_input_info" : \
                  { "index":'        + str(obj.index)  + ','   + \
                    '"name":"'       + obj.name        + '",'  + \
                    '"sink":'        + str(obj.sink)   + ','   + \
                    '"mute":'        + str(obj.mute)   + ','   + \
                    '"proplist":'    + object2json(obj.proplist)   + ','  + \
                    '"cvolume":'     + object2json(obj.volume) + '}}'
   return json_str

def source_output_info2json(obj):
   json_str = '{ "source_output_info" : \
                  { "index":'        + str(obj.index)  + ','   + \
                    '"name":"'       + obj.name        + '",'  + \
                    '"source":'      + str(obj.source)   + ','   + \
                    '"mute":'        + str(obj.mute)   + ','   + \
                    '"proplist":'    + object2json(obj.proplist)   + ','  + \
                    '"cvolume":'     + object2json(obj.volume) + '}}'
   return json_str

# outputs a string like { "channels" : 2, "values" : [1.0, 1.0] }
def cvolume2json(obj):
   json_str =  '{ "channels" :' + str(len(obj.values)) + ' , "values" :' + str(obj.values) + '}'
   return json_str

type2json_func = {
   list                                 : list2json,
   dict                                 : dict2json,
   pulsectl.pulsectl.PulseServerInfo    : server_info2json,
   pulsectl.pulsectl.PulseCardInfo      : card_info2json,
   pulsectl.pulsectl.PulseCardProfileInfo : card_profile_info2json,
   pulsectl.pulsectl.PulseSinkInfo      : sink_info2json,
   pulsectl.pulsectl.PulseSourceInfo    : source_info2json,
   pulsectl.pulsectl.PulseVolumeInfo    : cvolume2json,
   pulsectl.pulsectl.PulseSinkInputInfo : sink_input_info2json,
   pulsectl.pulsectl.PulseSourceOutputInfo : source_output_info2json
}

def object2json(obj):
   func=type2json_func.get(type(obj), unsupported_type2json)
   return func(obj)
##################  END OF CONVERSION FUNCTIONS #######################################
   
if __name__ == '__main__':
    try:
        print("Starting pulseaudio2mqtt service ...")

        # connect to pulseaudio server
        pulse = pulsectl.Pulse('pulseaudio2mqtt')

        # MQTT client setup
        mqttBroker= "localhost" if ( os.environ.get("mqtt_broker") is None ) else os.environ["mqtt_broker"]
        mqttPort  =  1883  if ( os.environ.get("mqtt_port")   is None ) else int(os.environ["mqtt_port"])

        def on_mqtt_connect(client, userdata, flags, rc):
           print("MQTT Connected With Result Code "+rc)

        def on_mqtt_message(client, userdata, message):
           print("WARNING: unsupported MQTT command received: ["+ message.topic+"] "+str(message.payload))

        def on_mqtt_get_card_list(client, userdata, message):
           print("MQTT: get_card_list_received: ["+ message.topic+"] "+str(message.payload))
           cardList=pulse.card_list()
           print(object2json(cardList))
           mqttClient.publish("pulseaudio2mqtt/cmd_rsp/get_card_list",
                           object2json(cardList),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered

        def on_mqtt_get_server_info(client, userdata, message):
           print("MQTT: get_server_info received: ["+ message.topic+"] "+str(message.payload))
           serverInfo=pulse.server_info()
           print(object2json(serverInfo))
           mqttClient.publish("pulseaudio2mqtt/cmd_rsp/get_server_info",
                           object2json(serverInfo),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered

        def on_mqtt_get_sink_info_list(client, userdata, message):
           print("MQTT: get_sink_info_list received: ["+ message.topic+"] "+str(message.payload))
           sinkList=pulse.sink_list()
           print(object2json(sinkList))
           mqttClient.publish("pulseaudio2mqtt/cmd_rsp/get_sink_info_list",
                           object2json(sinkList),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered

        def on_mqtt_get_source_info_list(client, userdata, message):
           print("MQTT: get_source_info_list received: ["+ message.topic+"] "+str(message.payload))
           sourceList=pulse.source_list()
           print(object2json(sourceList))
           mqttClient.publish("pulseaudio2mqtt/cmd_rsp/get_source_info_list",
                           object2json(sourceList),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered

        def on_mqtt_get_sink_input_info_list(client, userdata, message):
           print("MQTT: get_sink_input_info_list message received: ["+ message.topic+"] "+str(message.payload))
           sinkInputList=pulse.sink_input_list()
           print(object2json(sinkInputList))
           mqttClient.publish("pulseaudio2mqtt/cmd_rsp/get_sink_input_info_list",
                           object2json(sinkInputList),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered
                     
        def on_mqtt_get_source_output_info_list(client, userdata, message):
           print("MQTT: get_source_output_info_list message received: ["+ message.topic+"] "+str(message.payload))
           sourceOutputList=pulse.source_output_list()
           print(object2json(sourceOutputList))
           mqttClient.publish("pulseaudio2mqtt/cmd_rsp/get_source_output_info_list",
                           object2json(sourceOutputList),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered

        mqttClient=mqtt.Client("pulseaudio2mqtt")
        mqttClient.on_connect = on_mqtt_connect # on_connect doesn't seem to work ??
        mqttClient.on_message = on_mqtt_message
        mqttClient.connect(mqttBroker,mqttPort)

        mqttClient.subscribe("pulseaudio2mqtt/cmd/#", qos=1)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get_server_info", on_mqtt_get_server_info)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get_card_list", on_mqtt_get_card_list)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get_sink_info_list", on_mqtt_get_sink_info_list)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get_source_info_list", on_mqtt_get_source_info_list)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get_sink_input_info_list", on_mqtt_get_sink_input_info_list)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get_source_output_info_list", on_mqtt_get_source_output_info_list)

        # Publish the details of the device we are listening to
        mqttClient.publish("pulseaudio2mqtt",
                           "pulseaudio2mqtt service started at " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                           2,    # qos= 2 - deliver exactly once
                           True) # tell broker to retain this message so that it gets delivered

        # start the mqtt loop
        mqttClient.loop_forever()


    # all exceptions are handled !
    except Exception as error:
        print(error)

    print("sleeping 1 day...")
    time.sleep(3600*24)