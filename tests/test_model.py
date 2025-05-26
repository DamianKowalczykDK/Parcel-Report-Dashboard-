from src.model import (
    User,
    Locker,
    Parcel,
    Deliver,
    UsersDataDict,
    LockersDataDict,
    ParcelsDataDict,
    DeliversDataDict,
    CompartmentsLarge
)
import pytest

def test_user_to_dict(user_1: User, user_1_data: UsersDataDict) -> None:
    data = user_1.to_dict()
    assert data == user_1_data

def test_locker_to_dict(locker_1: Locker, locker_1_data: LockersDataDict) -> None:
    data = locker_1.to_dict()
    assert data == locker_1_data

def test_parcel_to_dict(parcel_1: Parcel, parcel_1_data: ParcelsDataDict) -> None:
    data = parcel_1.to_dict()
    assert data == parcel_1_data

def test_deliver_to_dict(deliver_1: Deliver, deliver_1_data: DeliversDataDict) -> None:
    data = deliver_1.to_dict()
    assert data == deliver_1_data

@pytest.mark.parametrize('height, length, expected', [
    (10, 30, CompartmentsLarge.SMALL),
    (30, 45, CompartmentsLarge.MEDIUM),
    (35, 60, CompartmentsLarge.LARGE),
])
def test_size_parcel(height: int, length: int, expected: CompartmentsLarge) -> None:
    data = Parcel.get_size(height, length)
    assert data == expected