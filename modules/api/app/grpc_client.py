import logging
import grpc
import udaconnect_pb2
import udaconnect_pb2_grpc
import udaconnect_pb2
import udaconnect_pb2_grpc

from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

class GRPCClient(object):

    def config(self, location_host, location_port, person_host, person_port):
        logger.info(f'grpc client - location: {location_host}:{location_port} person: {person_host}:{person_port}')

        # instantiate channels
        self.location_channel = grpc.insecure_channel('{}:{}'.format(location_host, location_port))
        self.person_channel = grpc.insecure_channel('{}:{}'.format(person_host, person_port))

        # bind the client and the server
        self.locationStub = udaconnect_pb2_grpc.LocationServiceStub(self.location_channel)
        self.personsStub = udaconnect_pb2_grpc.PersonServiceStub(self.person_channel)
        self.connectionStub = udaconnect_pb2_grpc.ConnectionServiceStub(self.person_channel)

        logger.info(f'grpc bind complete')

    def get_connections(self, person_id: int, start_date: datetime, end_date: datetime, distance: int):
        logger.info(f'get_connections - person_id: {person_id}-{type(person_id)} start_date: {start_date} end_date: {end_date} distance: {distance}-{type(distance)}')
        response = self.connectionStub.FindContacts(udaconnect_pb2.ConnectionRequest(id=person_id, start_date=start_date, end_date=end_date, distance=distance))
        return response

    def get_location(self, location_id: int):
        response = self.locationStub.Retrieve(udaconnect_pb2.LocationRequest(id=int(location_id)))
        return response

    def create_person(self, person):
        response = self.personsStub.Create(person)
        return response

    def get_person(self, person_id: int):
        response = self.personsStub.Retrieve(udaconnect_pb2.PersonRequest(id=int(person_id)))
        return response

    def get_person_all(self):
        response = self.personsStub.RetrieveAll(udaconnect_pb2.Empty())
        return response