import pulsectl, json, os, time
import paho.mqtt.client as mqtt
from datetime import datetime

pulse = pulsectl.Pulse('pulseaudio2mqtt')


if __name__ == '__main__':
    try:
        print("Starting pulseaudio2mqtt service ...")

        # connect to pulseaudio server
        pulse = pulsectl.Pulse('pulseaudio2mqtt')

        # MQTT client setup
        mqttBroker= "mqtt" if ( os.environ.get("mqtt_broker") is None ) else os.environ["mqtt_broker"]
        mqttPort  =  1883  if ( os.environ.get("mqtt_port")   is None ) else int(os.environ["mqtt_port"])

        def on_mqtt_connect(client, userdata, flags, rc):
           print("MQTT Connected With Result Code "+rc)

        def on_mqtt_message(client, userdata, message):
           print("WARNING: unsupported MQTT command received: ["+ message.topic+"] "+str(message.payload))

        def on_mqtt_get_sinks(client, userdata, message):
           print("MQTT_get_sinks message received: ["+ message.topic+"] "+str(message.payload))
           sinkList=pulse.sink_list()
           print(str(sinkList))
           mqttClient.publish("pulseaudio2mqtt/cmd-rsp/get-sinks",
                           str(sinkList),
                           1,    # qos= 2 - deliver exactly once
                           False) # tell broker to retain this message so that it gets delivered


        mqttClient=mqtt.Client("pulseaudio2mqtt")
        mqttClient.on_connect = on_mqtt_connect # on_connect doesn't seem to work ??
        mqttClient.on_message = on_mqtt_message
        mqttClient.connect(mqttBroker,mqttPort)

        mqttClient.subscribe("pulseaudio2mqtt/cmd/#", qos=1)
        mqttClient.message_callback_add("pulseaudio2mqtt/cmd/get-sinks", on_mqtt_get_sinks)

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
