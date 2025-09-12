import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "mosquitto"  # nombre del servicio en docker-compose
PORT = 1883
TOPIC = "sensors/ambient"
RETRIES = 10
DELAY = 3 # segundos

client = mqtt.Client()
#client.connect(BROKER, PORT, 60)
#
#try:
#    while True:
#        data = {
#           "temperature": round(random.uniform(18, 30), 2),
#           "humidity": round(random.uniform(40, 70), 2),
#            "timestamp": time.time()
#        }
#        payload = json.dumps(data)
#        client.publish(TOPIC, payload)
#        print(f"Publicado: {payload}")
#        time.sleep(5)
#except KeyboardInterrupt:
#    print("Sensor detenido.")
#finally:
#    client.disconnect()

for attempt in range(RETRIES):
    try:
        client.connect(BROKER, PORT, 60)
        print("Conectado a Mosquitto")

        while True:
            data = {
            "temperature": round(random.uniform(18, 30), 2),
            "humidity": round(random.uniform(40, 70), 2),
            "timestamp": time.time()
            }
            payload = json.dumps(data)
            client.publish(TOPIC, payload)
            print(f"Publicado: {payload}")
            time.sleep(5)

        #break
    except Exception as e:
        print(f"Intento {attempt+1}/{RETRIES} fallido: {e}")
        time.sleep(DELAY)
else:
    print("No se pudo conectar a Mosquitto después de varios intentos.")
    exit(1)

# ...continúa con el resto de tu código...
