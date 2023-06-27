import os
import json

from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
TOPIC_NAME = 'location_create'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

print("Sending sample payload...")

# new_location = Location()
# new_location.person_id = 1
# new_location.creation_time = '2020-08-15 10:37:06.000000'
# new_location.coordinate = '010100000097FDBAD39D925EC0D00A0C59DDC64240'

#location = {"person_id": 1, "creation_time": "2020-08-15 10:37:06.000000", "latitude": "-122.1", "longitude": "37.5"}
location = {"person_id": 1, "creation_time": "2020-08-15 10:37:06.000000", "latitude": "35.0585136", "longitude": "-106.5719566"}

jlocation = json.dumps(location)
print(f"dump - location: {location}-{type(location)} jlocation: {jlocation}-{type(jlocation)}")

#producer.send(TOPIC_NAME, b'Test Message!!!')
producer.send(TOPIC_NAME, bytes(jlocation, 'utf-8'))
producer.flush()
