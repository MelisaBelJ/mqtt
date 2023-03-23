from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
from enum import Enum
import paho.mqtt.publish as publish
import time

def on_message(mqttc, userdata, msg):
    print(f"Mensaje de {msg.topic} {msg.payload}")
    
def on_log(mqttc,userdata, level, string):
    print("Log:", string)
    
def main(broker):
    mqttc = Client(client_id = 'Productor', userdata={})
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)

    for t in Topics:
        mqttc.subscribe(t.getTopic())
        
    mqttc.loop_start()
    tests = [
        Mensaje(Topics.t1, 1, 'm1'),
        Mensaje(Topics.t2, 2, 'm2'),
        Mensaje(Topics.t1, 3, 'm3'),
        Mensaje(Topics.t2, 2, 'm4')
    ]
    for mensaje in tests:
        mqttc.publish('clients/PruebaP1Fin', mensaje.__str__())
    time.sleep(9)

class Mensaje():
    def __init__(self, res, t, m):
        self.res, self.t, self.m = res, t, m
        
    def __str__(self):
        return f'{self.res.getTopic()}, {self.t}, {self.m}'

class Topics(Enum):
    t1 = 'clients/PruebaP1a'
    t2 = 'clients/PruebaP1b'
    
    def getTopic(self):
        return self.value
if __name__ == "__main__":
    hostname = 'simba.fdi.ucm.es'
    main(hostname)
