from src.model import User, UsersDataDict, LockersDataDict, Locker, ParcelsDataDict, DeliversDataDict, Deliver, Parcel
from dataclasses import dataclass, field
from src.file_service import FileReader
from collections import defaultdict
from src.converter import Converter
from src.validator import Validator
import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class DataRepository[T, U]:
    """
    Generic repository class for loading, validating, and converting data_json from files.

    Attributes:
        file_reader (FileReader[T]): Reader to load raw data_json.
        validator (Validator[T]): Validator for raw data_json.
        converter (Converter[T, U]): Converter from raw data_json to model.
        filename (str | None): File path to read data_json from.
        _data (list[U]): Cached list of validated and converted data_json.
    """
    file_reader: FileReader[T]
    validator: Validator[T]
    converter: Converter[T, U]
    filename: str | None = None
    _data: list[U] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Post-initialization to ensure filename is set and data_json is loaded.
        Raises:
            ValueError: If filename is not provided.
        """
        if self.filename is None:
            raise ValueError("No filename set")
        self.refresh_data(self.filename)

    def get_data(self) -> list[U]:
        """
        Returns the cached list of data_json.

        Returns:
            list[U]: List of validated and converted data_json.
        """
        if not self._data:
            logging.warning("No data_json available")
        return self._data

    def refresh_data(self, filename: str | None = None) -> list[U]:
        """
        Refreshes the cached data_json from the given filename or from the existing filename.

        Args:
            filename (str | None): Optional new filename to load data_json from.

        Returns:
            list[U]: List of validated and converted data_json.
        """
        if filename is None:
            logging.warning(f"No provided filename used default filename")
        else:
            self.filename = filename
        logging.info(f"Refreshing {self.filename}")
        self._data = self._process_data(str(self.filename))
        return self._data

    def _process_data(self, filename: str) -> list[U]:
        """
        Reads raw data_json from file, validates and converts entries.

        Args:
            filename (str): Path to the file with raw data_json.

        Returns:
            list[U]: List of validated and converted data_json.
        """
        logging.info(f"Reading data_json from {filename}")
        raw_data = self.file_reader.read(filename)
        valid_data = []
        for entry in raw_data:
            if self.validator.validate(entry):
                converted_entry = self.converter.convert(entry)
                valid_data.append(converted_entry)
            else:
                logging.error(f"Invalid entry: {entry}")
        return valid_data


class UserDataRepository(DataRepository[UsersDataDict, User]):
    """
    Repository for user data_json.
    """
    pass


class LockerDataRepository(DataRepository[LockersDataDict, Locker]):
    """
    Repository for locker data_json.
    """
    pass


class ParcelDataRepository(DataRepository[ParcelsDataDict, Parcel]):
    """
    Repository for parcel data_json.
    """
    pass


class DeliveryDataRepository(DataRepository[DeliversDataDict, Deliver]):
    """
    Repository for delivery data_json.
    """
    pass


@dataclass
class ParcelSummaryRepository[U, L, P, D]:
    """
    Aggregates and summarizes parcel delivery data_json across multiple repositories.

    Attributes:
        user_repo (DataRepository[U, User]): Repository of users.
        locker_repo (DataRepository[L, Locker]): Repository of lockers.
        parcel_repo (DataRepository[P, Parcel]): Repository of parcels.
        delivery_repo (DataRepository[D, Deliver]): Repository of deliveries.
        _parcel_summary (dict[str, dict[str, int]]): Cached parcel summary.
    """
    user_repo: DataRepository[U, User]
    locker_repo: DataRepository[L, Locker]
    parcel_repo: DataRepository[P, Parcel]
    delivery_repo: DataRepository[D, Deliver]
    _parcel_summary: dict[str, dict[str, int]] = field(default_factory=dict, init=False)

    def parcel(self, force_refresh: bool = False) -> dict[str, dict[str, int]]:
        """
        Returns the parcel summary, optionally forcing a refresh.

        Args:
            force_refresh (bool): If True, rebuilds the summary even if cached.

        Returns:
            dict[str, dict[str, int]]: Mapping of parcel IDs to locker IDs and counts.
        """
        if force_refresh or not self._parcel_summary:
            logging.info("Building or refreshing parcel summary from repository")
            self._parcel_summary = self._build_parcel()
        return self._parcel_summary

    def _build_parcel(self) -> dict[str, dict[str, int]]:
        """
        Builds the parcel summary by cross-referencing users, lockers, parcels, and deliveries.

        Returns:
            dict[str, dict[str, int]]: Mapping of parcel IDs to locker IDs and counts.
        """
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
                parcel_summary[parcel.parcel_id][locker.locker_id] += 1
            else:
                logging.warning(f"Parcel {deliver.parcel_id} not available")

        return parcel_summary
