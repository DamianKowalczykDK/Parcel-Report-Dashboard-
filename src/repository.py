from src.model import User, UsersDataDict, LockersDataDict, Locker, ParcelsDataDict, DeliversDataDict, Deliver, Parcel
from dataclasses import dataclass, field
from src.file_service import FileReader
from collections import defaultdict
from src.converter import Converter
from src.validator import Validator
from typing import Any
import logging

logging.basicConfig(level=logging.INFO)


@dataclass
class DataRepository[T, U]:
    file_reader: FileReader[T]
    validator: Validator[T]
    converter: Converter[T, U]
    filename: str | None = None
    _data: list[U] = field(default_factory=list)


    def __post_init__(self) -> None:
        if self.filename is None:
            raise ValueError("No filename set")
        self.refresh_data(self.filename)

    def get_data(self) -> list[U]:
        if not self._data:
            logging.warning("No data available")
        return self._data

    def refresh_data(self, filename: str | None = None) -> list[U]:
        if filename is None:
            logging.warning(f'No provided filename used default filename')
        else:
            self.filename = filename
        logging.info(f'Refreshing {self.filename}')
        self._data = self._process_data(str(self.filename))
        return self._data

    def _process_data(self, filename: str) -> list[U]:
        logging.info(f'Reading data from {filename}')
        raw_data = self.file_reader.read(filename)
        valid_data = []
        for entry in raw_data:
            if self.validator.validate(entry):
                converted_entry = self.converter.convert(entry)
                valid_data.append(converted_entry)
            else:
                logging.error(f'Invalid entry: {entry}')
        return valid_data



class UserDataRepository(DataRepository[UsersDataDict, User]):
    pass

class LockerDataRepository(DataRepository[LockersDataDict, Locker]):
    pass

class ParcelDataRepository(DataRepository[ParcelsDataDict, Parcel]):
    pass

class DeliveryDataRepository(DataRepository[DeliversDataDict, Deliver]):
    pass

@dataclass
class ParcelSummaryRepository[U, L, P, D]:
    user_repo: DataRepository[U, User]
    locker_repo: DataRepository[L, Locker]
    parcel_repo: DataRepository[P,Parcel]
    delivery_repo: DataRepository[D,Deliver]
    _parcel_summary: dict[Any, Any] = field(default_factory=dict, init=False)

    def parcel(self, force_refresh: bool = False) -> dict[Any, Any]:
        if force_refresh or not self._parcel_summary:
            logging.info(f'Building or refreshing parcel summary from repository')
            self._parcel_summary = self._build_parcel()
        return self._parcel_summary

    def _build_parcel(self) -> dict[Any, Any]:
        parcel_summary: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

        users = {user.email: user for user in self.user_repo.get_data()}
        lockers = {locker.locker_id: locker for locker in self.locker_repo.get_data()}
        parcels = {parcel.parcel_id: parcel for parcel in self.parcel_repo.get_data()}
        delivers = self.delivery_repo.get_data()

        for deliver in delivers:
            parcel = parcels.get(deliver.parcel_id)
            locker = lockers.get(deliver.locker_id)
            sender = users.get(deliver.sender_email)
            receiver = users.get(deliver.receiver_email)

            if parcel and locker and sender and receiver:
                parcel_summary[locker.locker_id][parcel.parcel_id] += 1
            else:
                logging.warning(f'Parcel {deliver.parcel_id} not available')

        return parcel_summary




