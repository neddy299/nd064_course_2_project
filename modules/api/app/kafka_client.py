import logging
import json
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

TOPIC_NAME = 'location_create'

class KafkaClient(object):

    def config(self, host, port):
        self.host = host
        self.server_port = port

        logger.info(f'kafka client - host: {host} port: {port}')

        self.producer = KafkaProducer(bootstrap_servers='{}:{}'.format(self.host, self.server_port))

        logger.info(f'kafka bind complete')

    def create_location(self, location):
        self.producer.send(TOPIC_NAME, bytes(json.dumps(location), 'utf-8'))
        self.producer.flush()
