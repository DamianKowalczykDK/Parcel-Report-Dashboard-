from src.model import Deliver, User, Parcel, Locker
from src.service import ParcelReportService
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def service(mock_repository: MagicMock) -> ParcelReportService:
    return ParcelReportService(repository=mock_repository)

@pytest.fixture
def delivers_list(deliver_1: Deliver, deliver_2: Deliver) -> list[Deliver]:
    return [deliver_1, deliver_2]

@pytest.fixture
def users_list(user_1: User, user_2: User) -> list[User]:
    return [user_1, user_2]

@pytest.fixture
def parcels_list(parcel_1: Parcel, parcel_2: Parcel) -> list[Parcel]:
    return [parcel_1, parcel_2]

@pytest.fixture
def lockers_list(locker_1: Locker, locker_2: Locker) -> list[Locker]:
    return [locker_1, locker_2]