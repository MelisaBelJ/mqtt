from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep

def lee(mensaje, broker):
    res, t ,m = mensaje.split(', ')
    print(f'Procesando... {t}, {res}, {m}')
    sleep(int(t))
    publish.single(res, payload=m, hostname=broker)
    print('Fin proceso', mensaje)

def on_message(mqttc, userdata, msg):
    print(f'Mensaje de {msg.topic}: {msg.payload}')
    Process(target=lee, args=(str(msg.payload)[2:-1], userdata['broker'])).start()
     
def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)
    
def on_connect(mqttc, userdata, flags, rc):
 print("CONNECT:", userdata, flags, rc)

def main(hostname):
    userdata = {'broker': hostname }
    mqttc = Client(userdata=userdata)
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect(hostname)
    
    mqttc.subscribe('clients/PruebaP1Fin')
    mqttc.loop_forever()

if __name__ == "__main__":
    hostname = 'simba.fdi.ucm.es'
    main(hostname)
