from src.repository import UserDataRepository, LockerDataRepository, ParcelDataRepository, DeliveryDataRepository
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def file_reader_mock() -> MagicMock:
    return MagicMock()

@pytest.fixture
def validator_mock() -> MagicMock:
    return MagicMock()

@pytest.fixture
def converter_mock() -> MagicMock:
    return MagicMock()

@pytest.fixture
def user_data_repository(file_reader_mock, validator_mock, converter_mock) -> UserDataRepository:
    return UserDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename="user.json",
    )

@pytest.fixture
def locker_data_repository(file_reader_mock, validator_mock, converter_mock) -> LockerDataRepository:
    return LockerDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename="locker.json",
    )

@pytest.fixture
def parcel_data_repository(file_reader_mock, validator_mock, converter_mock) -> ParcelDataRepository:
    return ParcelDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename="parcel.json",
    )

@pytest.fixture
def deliver_data_repository(file_reader_mock, validator_mock, converter_mock) -> DeliveryDataRepository:
    return DeliveryDataRepository(
        file_reader=file_reader_mock,
        validator=validator_mock,
        converter=converter_mock,
        filename="delivery.json",
    )

