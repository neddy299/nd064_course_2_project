from kafka import KafkaConsumer

from app.udaconnect.controllers import LocationConsumer


def serve(host, port):
    consumer = KafkaConsumer(bootstrap_servers='{}:{}'.format(host, port))
    location = LocationConsumer()

    # TODO: spin out threads for each consumer
    location.Create(consumer)
