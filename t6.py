from paho.mqtt.client import Client
from multiprocessing import Process, Manager
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from time import sleep
import random
from paho.mqtt.client import Client

def on_message(client, userdata, msg):
    print(f'Mensaje de {msg.topic}: {msg.payload}')
    try:
        n =  int(msg.payload)
        userdata['entero'] += 1
        if userdata['entero'] %5 == 0:
            publish.single('clients/PruebaP1Enteros', payload=f"{userdata['entero']} enteros leidos, suponen un {(100*userdata['entero']) /(userdata['entero'] + userdata['real'] )} % del total", hostname=userdata['broker'])
    except ValueError:
        userdata['real'] += 1
        if userdata['real'] %5 == 0:
            publish.single('clients/PruebaP1Reales', payload=f"{userdata['real']} reales leidos, suponen un {(100*userdata['real']) /(userdata['entero'] + userdata['real'] )} % del total", hostname=userdata['broker'])
    except Exception as e:
        raise e        

def main(hostname, topic):
    userdata = {'entero':0, 'real':0, 'broker':hostname}
    client = Client(userdata=userdata)
    client.on_message = on_message
    client.connect(hostname)
    client.subscribe(topic)
    client.loop_forever()
    
if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    topic = 'numbers'
    main(hostname, topic)
