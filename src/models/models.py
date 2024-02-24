from src.exceptions.exceptions import *
from dataclasses import dataclass


@dataclass
class Location:
    longitude: float
    latitude: float

    def __init__(self, longitude: float, latitude: float) -> None:
        if -180 <= longitude <= 180:
            self.longitude = longitude
        else:
            raise InvalidLongitudeException(longitude)

        if -90 <= latitude <= 90:
            self.latitude = latitude
        else:
            raise InvalidLatitudeException(latitude)


@dataclass
class Stop:
    name: str
    location: Location
    post: str
    street_id: str
    group_id: str

    def __hash__(self):
        return hash(
            (self.name, self.location.longitude, self.location.latitude, self.post, self.street_id, self.group_id))

    def __eq__(self, other):
        if not isinstance(other, Stop):
            return False
        return (self.name, self.location.longitude, self.location.latitude, self.post, self.street_id, self.group_id) == \
            (other.name, other.location.longitude, other.location.latitude, other.post, other.street_id, other.group_id)
