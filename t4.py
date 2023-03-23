from paho.mqtt.client import Client
from enum import Enum
class Topics(Enum):
    T = 'temperature/t1'
    H = 'humidity'
    
    def getTopic(self):
        return self.value
        
    def getLimite(self):
        return 20 if self == Topics.T else 60

def on_message(mqttc, userdata, msg):
    print(f'message:{msg.topic}:{msg.payload}:{userdata}')
    valor = int(msg.payload)
    if userdata['conH'] == 0 and valor > Topics.T.getLimite():
            print(f'{valor}, supera el límite de temperatura, suscrito a humedad')
            userdata['conH'] = 1
            mqttc.subscribe(Topics.H.getTopic())
    elif userdata['conH'] == 1 :
        if msg.topic == Topics.H.value and valor > Topics.H.getLimite():
                print(f'{valor}, supera el límite de humedad, desuscrito de humedad')
                userdata['conH'] = 0
                mqttc.unsubscribe(Topics.H.getTopic())
        elif Topics.T.value in msg.topic and valor < Topics.T.getLimite():
                print(f'{valor}, supera el límite de temperatura, desuscrito de humedad')
                userdata['conH'] = 0
                mqttc.unsubscribe(Topics.H.getTopic())

def on_log(mqttc, userdata, level, buf):
    print(f'LOG:{userdata}:{msg}')
    
def main(hostname):
    userdata = {'conH':0}
    mqttc = Client(userdata=userdata)
    mqttc.on_message = on_message
    mqttc.enable_logger()
    
    mqttc.connect(hostname)
    mqttc.subscribe(Topics.T.getTopic())
    mqttc.loop_forever()
    

if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    main(hostname)
