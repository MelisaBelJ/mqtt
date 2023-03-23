import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import sys

def publicar(hostname, topic):
    while True:
        data  = input('Mensaje: ')
        print(f"Publicando {data} en :{topic}:")
        publish.single(topic,  data, hostname=hostname)
    
def suscribir(hostname, topic):
    n_msg = int(input('Cuántos mensajes? '))

    print(f"Subcribing :{topic}:, {n_msg} messages")
    msgs = subscribe.simple(topic, 
                            msg_count = n_msg,
                            hostname = hostname)

    if n_msg == 1:
        print(msgs.topic, msgs.payload.decode('utf8'))
    else:
        for m in msgs:
            print(m.topic, m.payload.decode('utf8'))

if __name__ == "__main__":
    hostname = 'simba.fdi.ucm.es'
    topic = '/clients/PruebaP1'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    if input('Susbcribir o publicar?').lower() == 'suscribir':
        suscribir(hostname, topic)
    else:
        publicar(hostname, topic)
    
