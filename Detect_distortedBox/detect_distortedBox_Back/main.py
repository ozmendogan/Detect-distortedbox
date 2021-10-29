import paho.mqtt.client as mqtt
import utilities
import dcmotor


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.payload.decode("utf-8"))
    
    if msg.payload.decode("utf-8")=="start":
        
        dcmotor.motorStart()
        utilities.shapeDetection()
    
        
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("admin", "password")
client.connect("broker", 8883)


client.subscribe("mydevice")

client.loop_forever()
