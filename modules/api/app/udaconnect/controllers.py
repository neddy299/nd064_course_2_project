from datetime import datetime

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app import grpcClient, kafkaClient
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

import udaconnect_pb2

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        kafkaClient.create_location(request.get_json())

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        response = grpcClient.get_location(location_id)
        location = Location(id=response.id, person_id=response.person_id, 
                            coordinate=response.coordinate, wkt_shape=response.wkt_shape,
                            creation_time=datetime.fromisoformat(response.creation_time))
        return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person = udaconnect_pb2.PersonMessage(first_name=payload["first_name"], last_name=payload["last_name"], company_name=payload["company_name"])
        response = grpcClient.create_person(new_person)
        return Person(id=response.id, first_name=response.first_name, last_name=response.last_name, company_name=response.company_name)

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        response = grpcClient.get_person_all()
        persons: List[Person] = []
        for p in response.persons:
            person = Person(id=p.id, first_name=p.first_name, last_name=p.last_name, company_name=p.company_name)
            persons.append(person)
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        response = grpcClient.get_person(person_id)
        person = Person(id=response.id, first_name=response.first_name, last_name=response.last_name, company_name=response.company_name)        
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        distance: Optional[int] = request.args.get("distance", 5)
        response = grpcClient.get_connections(
            person_id=person_id,
            start_date=request.args["start_date"],
            end_date=request.args["end_date"],
            distance=distance,
        )
        results: List[Connection] = []
        for conn in response.connections:
            person = Person(id=conn.person.id, first_name=conn.person.first_name, last_name=conn.person.last_name, company_name=conn.person.company_name)
            location = Location(id=conn.location.id, person_id=conn.location.person_id, 
                coordinate=conn.location.coordinate, wkt_shape=conn.location.wkt_shape,
                creation_time=datetime.fromisoformat(conn.location.creation_time))
            connection = Connection(location=location, person=person)
            results.append(connection)
        return results
