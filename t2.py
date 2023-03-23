from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
import random
from paho.mqtt.client import Client

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n =  int(msg.payload)
        userdata['entero'] += 1
    except ValueError:
        userdata['real'] += 1
    except Exception as e:
        raise e
    print((100*userdata['entero']) /(userdata['entero'] +userdata['real'] ), '% enteros')

def main(broker, topic):
    userdata = {'entero':0, 'real':0}
    client = Client(userdata=userdata)
    client.on_message = on_message
    client.connect(broker)
    client.subscribe(topic)
    client.loop_forever()
    
if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    topic = 'numbers'
    main(hostname, topic)
