#########################################  MQTT BASIC
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
MQTT_SERVER = "192.168.43.175"
MQTT_PATH = "test"

publish.single(MQTT_PATH, 'y', hostname=MQTT_SERVER)

def on_connect(client, userdata, flags, rc):
     print("connected with result code "+str(rc))
     client.subscribe(MQTT_PATH)
def on_message(client, userdata, msg):
     print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()


