from paho.mqtt.client import Client
from multiprocessing import Process, Manager, Lock
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from time import sleep
import random
from paho.mqtt.client import Client

def media(datos):
    r = 0
    for x in datos:
        r += int(x)
    return r/len(datos)

def on_message2(client2, userdata2, msg):
    print(f'Mensaje de {msg.topic}: {msg.payload}')
    if 'humidity' in msg.topic:
        with userdata2['lock']:
            userdata2['datos'].append(msg.payload)
    else:
        cantidad = int(str(msg.payload)[2:].split(' ')[0])
        if userdata2['activo'] == 0:
            if cantidad %10 == 0 and 'Entero' in msg.topic:
                    client2.subscribe('humidity')
                    userdata2['activo'] = 1
                    print('Suscrito a humidity')
        else:
            if cantidad %10 == 0 and 'Real' in msg.topic:
                    client2.unsubscribe('humidity')
                    userdata2['activo'] = 0
                    print('Desuscrito de humidity')

def main(hostname):
    userdata2 = {'activo':0, 'lock': Lock(), 'datos': []}
    client2 = Client(userdata=userdata2)
    client2.on_message = on_message2
    client2.connect(hostname)
    client2.subscribe('clients/PruebaP1Reales')
    client2.subscribe('clients/PruebaP1Enteros')
    client2.loop_start()
    
    while True:
        sleep(6)
        if userdata2['activo'] == 1:
            with userdata2['lock']:
                print(f"Media de humedad: {media(userdata2['datos'] )}")
                userdata2['datos'] = []
    
if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    main(hostname)
