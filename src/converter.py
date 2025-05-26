from src.model import (
    User,
    Locker,
    Parcel,
    Deliver,
    UsersDataDict,
    LockersDataDict,
    CompartmentsLarge,
    ParcelsDataDict,
    DeliversDataDict
)
from abc import ABC, abstractmethod
from typing import override


class Converter[T, U](ABC):
    @abstractmethod
    def convert(self, data: T) -> U:  # pragma: no cover
        pass

class UserConverter(Converter[UsersDataDict, User]):
    @override
    def convert(self, data: UsersDataDict) -> User:
        return User(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            city=data['city'],
            latitude=data['latitude'],
            longitude=data['longitude'],
        )

class LockerConverter(Converter[LockersDataDict, Locker]):
    @override
    def convert(self, data: LockersDataDict) -> Locker:
        compartment = data['compartments']
        converted_compartment = {CompartmentsLarge(key): value for key, value in compartment.items()}

        return Locker(
            locker_id=data['locker_id'],
            city=data['city'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            compartments=converted_compartment,
        )

class ParcelConverter(Converter[ParcelsDataDict, Parcel]):
    @override
    def convert(self, data: ParcelsDataDict) -> Parcel:
        return Parcel(
            parcel_id=data['parcel_id'],
            height=data['height'],
            length=data['length'],
            weight=data['weight'],
        )

class DeliverConverter(Converter[DeliversDataDict, Deliver]):
    @override
    def convert(self, data: DeliversDataDict) -> Deliver:
        return Deliver(
            parcel_id=data['parcel_id'],
            locker_id=data['locker_id'],
            sender_email=data['sender_email'],
            receiver_email=data['receiver_email'],
            sent_date=data['sent_date'],
            expected_delivery_date=data['expected_delivery_date'],
        )


