import os
import json

from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
TOPIC_NAME = 'location_create'

consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER)
consumer.subscribe([TOPIC_NAME])
for message in consumer:
    print (message)
    msg = message.value.decode('utf-8')
    data = json.loads(msg)
    print(f"dump - msg: {msg}-{type(msg)} data: {data}-{type(data)}")