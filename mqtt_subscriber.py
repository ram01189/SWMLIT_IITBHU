import paho.mqtt.client as mqtt
MQTT_SERVER = "192.168.43.175"
MQTT_PATH1 = "test"
#MQTT_PATH2 = "moisture/waterlevel"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH1)
    print("connected")
    #client.subscribe(MQTT_PATH2)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    mois=msg.payload
    print(str(mois))
    #time.sleep(2)
    # more callbacks, etc
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()

