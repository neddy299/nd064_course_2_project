import json
import logging

from app.udaconnect.models import Location
from app.udaconnect.services import LocationService

import udaconnect_pb2
import udaconnect_pb2_grpc

import logging

TOPIC_NAME_LOCATION_CREATE = 'location_create'


class LocationConsumer():
    def Create(self, consumer):
        print(f"starting location create consumeer")

        consumer.subscribe([TOPIC_NAME_LOCATION_CREATE])
        for message in consumer:
            msg = message.value.decode('utf-8')
            LocationService.create(json.loads(msg))

class LocationServicer(udaconnect_pb2_grpc.LocationServiceServicer):    
    def Retrieve(self, request, context):
        logging.info(f'retieving location for id: {request.id}')
        location: Location = LocationService.retrieve(request.id)
        result = udaconnect_pb2.LocationMessage(id=location.id, person_id=location.person_id, 
                                              coordinate=str(location.coordinate),
                                              wkt_shape=location.wkt_shape,
                                              creation_time=location.creation_time.isoformat())        
        return result          
