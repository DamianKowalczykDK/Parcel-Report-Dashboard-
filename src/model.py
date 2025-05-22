from dataclasses import dataclass
from typing import TypedDict
from enum import Enum

class CompartmentsLarge(Enum):
    """
        Enum representing available locker compartment sizes.
        """
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class UsersDataDict(TypedDict):
    """
        TypedDict representing the structure of user data.
        """
    email: str
    name: str
    surname: str
    city: str
    latitude: float
    longitude: float

class LockersDataDict(TypedDict):
    """
        TypedDict representing the structure of locker (parcel machine) data.

        compartments: dictionary with keys as compartment sizes (str)
        and values as integer counts.
        """
    locker_id: str
    city: str
    latitude: float
    longitude: float
    compartments: dict[str, int]

class ParcelsDataDict(TypedDict):
    """
        TypedDict representing the structure of parcel data.
        """
    parcel_id: str
    height: int
    length: int
    weight: int

class DeliversDataDict(TypedDict):
    """
        TypedDict representing the structure of a delivery record.

        sent_date and expected_delivery_date are expected to be in 'YYYY-MM-DD' format.
        """
    parcel_id: str
    locker_id: str
    sender_email: str
    receiver_email: str
    sent_date: str
    expected_delivery_date: str


@dataclass
class User:
    """
        Represents a system user with location information.
        """
    email: str
    name: str
    surname: str
    city: str
    latitude: float
    longitude: float

    def to_dict(self) -> UsersDataDict:
        """
                Converts the User instance into a dictionary matching the UserDataDict structure.
                """
        return {
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

@dataclass
class Locker:
    """
        Represents a parcel locker with compartments of various sizes.
        """
    locker_id: str
    city: str
    latitude: float
    longitude: float
    compartments: dict[CompartmentsLarge, int]

    def to_dict(self) -> LockersDataDict:
        """
                Converts the Locker instance into a dictionary matching the LockersDataDict structure,
                converting Enum keys to string values.
                """
        return {
            "locker_id": self.locker_id,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "compartments": {key.value: value for key, value in self.compartments.items()},
        }

@dataclass
class Parcel:
    """
        Represents a physical parcel with dimensions and weight.
        """
    parcel_id: str
    height: int
    length: int
    weight: int

    def to_dict(self) -> ParcelsDataDict:
        """
                Converts the Parcels instance into a dictionary matching the ParcelsDataDict structure.
                """
        return {
            "parcel_id": self.parcel_id,
            "height": self.height,
            "length": self.length,
            "weight": self.weight,
        }

@dataclass
class Deliver:
    """
        Represents a delivery operation between a sender and receiver.
        """
    parcel_id: str
    locker_id: str
    sender_email: str
    receiver_email: str
    sent_date: str
    expected_delivery_date: str

    def to_dict(self) -> DeliversDataDict:
        """
                Converts the Delivers instance into a dictionary matching the DeliversDataDict structure.
                """
        return {
            "parcel_id": self.parcel_id,
            "locker_id": self.locker_id,
            "sender_email": self.sender_email,
            "receiver_email": self.receiver_email,
            "sent_date": self.sent_date,
            "expected_delivery_date": self.expected_delivery_date,
        }

