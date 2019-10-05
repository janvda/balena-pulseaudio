import pulsectl, json, os, time
import paho.mqtt.client as mqtt
from datetime import datetime

pulse = pulsectl.Pulse('pa-mqtt')


if __name__ == '__main__':
    try:
        print("Starting pa-mqtt service ...")

        # connect to pulseaudio server
        pulse = pulsectl.Pulse('pa-mqtt')

        # MQTT client setup
        mqttBroker= "mqtt" if ( os.environ.get("mqtt_broker") is None ) else os.environ["mqtt_broker"]
        mqttPort  =  1883  if ( os.environ.get("mqtt_port")   is None ) else int(os.environ["mqtt_port"])

        mqttClient=mqtt.Client("pa-mqtt")
        mqttClient.connect(mqttBroker,mqttPort)
        mqttClient.loop_start()

        # Publish the details of the device we are listening to
        mqttClient.publish("pa-mqtt",
                           "pa-mqtt service started at " + datetime.now(),
                           2,    # qos= 2 - deliver exactly once
                           True) # tell broker to retain this message so that it gets delivered


    # all exceptions are handled !
    except Exception as error:
        print(error)

    print("sleeping 1 day...")
    time.sleep(3600*24)
