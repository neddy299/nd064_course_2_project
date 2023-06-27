from datetime import datetime
from concurrent import futures
from typing import Optional, List
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String

from app import Session
from app.udaconnect.models import Connection, Person
from app.udaconnect.services import ConnectionService, PersonService
import udaconnect_pb2
import udaconnect_pb2_grpc

DATE_FORMAT = "%Y-%m-%d"


class ConnectionServicer(udaconnect_pb2_grpc.ConnectionServiceServicer):
    def FindContacts(self, request, context):
        start_date: datetime = datetime.strptime(request.start_date, DATE_FORMAT)
        end_date: datetime = datetime.strptime(request.end_date, DATE_FORMAT)
        distance: Optional[int] = request.distance
        connections: List[Connection] = ConnectionService.find_contacts(person_id=request.id, start_date=start_date, end_date=end_date, meters=distance)
        result = udaconnect_pb2.ConnectionsMessageList()
        for row in connections:            
            location = udaconnect_pb2.LocationMessage(id=row.location.id, person_id=row.location.person_id,
                                                      coordinate=str(row.location.coordinate),
                                                      wkt_shape=row.location.wkt_shape,
                                                      creation_time=row.location.creation_time.isoformat())
            person = udaconnect_pb2.PersonMessage(id=row.person.id, first_name=row.person.first_name, 
                                                  last_name=row.person.last_name, company_name=row.person.company_name)
            connection = udaconnect_pb2.ConnectionMessage(location=location, person=person)
            result.connections.append(connection)
        return result  

class PersonServicer(udaconnect_pb2_grpc.PersonServiceServicer):
    def Create(self, request, context):
        request_value = {"id": request.id, "first_name": request.first_name, "last_name": request.last_name, "company_name": request.company_name}
        person: Person = PersonService.create(request_value)
        return udaconnect_pb2.PersonMessage(id=person.id, first_name=person.first_name, last_name=person.last_name, company_name=person.company_name)
    
    def Retrieve(self, request, context):
        person: Person = PersonService.retrieve(request.id)        
        result = udaconnect_pb2.PersonMessage(id=person.id, first_name=person.first_name, last_name=person.last_name, company_name=person.company_name)
        return result          

    def RetrieveAll(self, request, context):
        persons: List[Person] = PersonService.retrieve_all()
        result = udaconnect_pb2.PersonMessageList()
        for row in persons:            
            result.persons.append(udaconnect_pb2.PersonMessage(id=row.id, first_name=row.first_name, last_name=row.last_name, company_name=row.company_name))
        return result    
