from src.model import User, Locker, Parcel, Deliver, UsersDataDict, LockersDataDict, ParcelsDataDict, DeliversDataDict
from src.repository import ParcelSummaryRepository
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def mock_user_repo(user_1: User, user_2: User) -> MagicMock:
    repo = MagicMock()
    repo.get_data.return_value = [user_1, user_2]
    return repo

@pytest.fixture
def mock_locker_repo(locker_1: Locker, locker_2: Locker) -> MagicMock:
    repo = MagicMock()
    repo.get_data.return_value = [locker_1, locker_2]
    return repo

@pytest.fixture
def mock_parcel_repo(parcel_1: Parcel, parcel_2: Parcel) -> MagicMock:
    repo = MagicMock()
    repo.get_data.return_value = [parcel_1, parcel_2]
    return repo

@pytest.fixture
def mock_deliver_repo(deliver_1: Deliver, deliver_2: Deliver) -> MagicMock:
    repo = MagicMock()
    repo.get_data.return_value = [deliver_1, deliver_2]
    return repo

@pytest.fixture
def parcel_summary_repo(
        mock_user_repo: MagicMock,
        mock_locker_repo: MagicMock,
        mock_parcel_repo: MagicMock,
        mock_deliver_repo: MagicMock
) -> ParcelSummaryRepository[UsersDataDict, LockersDataDict, ParcelsDataDict, DeliversDataDict]:
    return ParcelSummaryRepository(
        user_repo=mock_user_repo,
        locker_repo=mock_locker_repo,
        parcel_repo=mock_parcel_repo,
        delivery_repo=mock_deliver_repo
    )
