import logging
from typing import Dict, List

from app import Session
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location")

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        session = Session()
        location, coord_text = (
            session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session = Session()
        session.add(new_location)
        session.commit()

        return new_location