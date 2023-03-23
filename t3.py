from threading import Lock
from paho.mqtt.client import Client
from time import sleep

def on_message(mqttc,userdata,msg):
    print ('on_message', msg.topic, msg.payload)
    with userdata['lock']:
        try:
            nombre = msg.topic[12:]
            if not nombre in userdata:
                userdata['datos'][nombre] = []
            userdata['datos'][nombre].append(msg.payload)
        except:
            pass
  
def media(datos):
    r = 0
    for x in datos:
        r += int(x)
    return r/len(datos)
    
def main(hostname, topic):
    userdata = {'lock': Lock(), 'datos':{}}
    mqttc = Client(userdata = userdata)
    mqttc.on_message = on_message
    mqttc.connect(hostname)
    mqttc.subscribe(topic)
    mqttc.loop_start()
    
    while True:
        sleep(6)
        with userdata['lock']:
            for nombre, datos in userdata['datos'].items():
                print(f'Media de {nombre}:{media(datos)}')
                userdata['datos'][nombre] = []
            
if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    topic = 'temperature/#'
    main(hostname, topic)
