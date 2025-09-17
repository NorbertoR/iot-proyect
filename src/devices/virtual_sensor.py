import time
import random
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

BROKER = "mosquitto"  # nombre del servicio en docker-compose
PORT = 1883
TOPIC = "sensors/ambient"
RETRIES = 10 # número de reintentos
DELAY = 3 # segundos

# Configuración de InfluxDB
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "mi-token-super-seguro"
INFLUXDB_ORG = "iot-org"
INFLUXDB_BUCKET = "iot"

influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

client = mqtt.Client(protocol=mqtt.MQTTv311)

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

            # Persistir en InfluxDB
            point = Point("ambient_sensor") \
                .field("temperature", data["temperature"]) \
                .field("humidity", data["humidity"]) \
                .time(int(data["timestamp"]), write_precision="s")
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

            time.sleep(5)

        #break
    except Exception as e:
        print(f"Intento {attempt+1}/{RETRIES} fallido: {e}")
        time.sleep(DELAY)
else:
    print("No se pudo conectar a Mosquitto después de varios intentos.")
    exit(1)

# ...continúa con el resto de tu código...
