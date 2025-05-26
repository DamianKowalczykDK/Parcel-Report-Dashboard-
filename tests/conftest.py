from unittest.mock import MagicMock
import pytest
from src.model import (
    User,
    Deliver,
    Locker,
    Parcel,
    UsersDataDict,
    CompartmentsLarge,
    LockersDataDict,
    ParcelsDataDict,
    DeliversDataDict
)

def fake_user() -> MagicMock:
    return MagicMock(spec=User)

@pytest.fixture
def user_1() -> User:
    return User(
        email="john.doe@example.com",
        name="John",
        surname="Doe",
        city="New York",
        latitude=40.712776,
        longitude=-74.005974
    )

@pytest.fixture
def user_1_data() -> UsersDataDict:
    return {
        "email": "john.doe@example.com",
        "name": "John",
        "surname": "Doe",
        "city": "New York",
        "latitude": 40.712776,
        "longitude": -74.005974
    }

@pytest.fixture
def user_2() -> User:
    return User(
        email="jane.smith@example.com",
        name="Jane",
        surname="Smith",
        city="Los Angeles",
        latitude=34.052235,
        longitude=-118.243683
    )

@pytest.fixture
def user_2_data() -> UsersDataDict:
    return {
        "email": "jane.smith@example.com",
        "name": "Jane",
        "surname": "Smith",
        "city": "Los Angeles",
        "latitude": 34.052235,
        "longitude": -118.243683
    }

@pytest.fixture
def locker_1() -> Locker:
    return Locker(
        locker_id="L001",
        city="New York",
        latitude=40.730610,
        longitude=-73.935242,
        compartments= {CompartmentsLarge.SMALL: 20, CompartmentsLarge.MEDIUM: 15, CompartmentsLarge.LARGE: 5}
    )

@pytest.fixture
def locker_1_data() -> LockersDataDict:
    return {
        "locker_id": "L001",
        "city": "New York",
        "latitude": 40.730610,
        "longitude": -73.935242,
        "compartments": {"small": 20, "medium": 15, "large": 5}
    }

@pytest.fixture()
def locker_2() -> Locker:
    return Locker(
        locker_id="L002",
        city="Los Angeles",
        latitude=34.052235,
        longitude=-118.243683,
        compartments={CompartmentsLarge.SMALL: 25, CompartmentsLarge.MEDIUM: 10, CompartmentsLarge.LARGE: 8}
    )

@pytest.fixture
def locker_2_data() -> LockersDataDict:
    return {
        "locker_id": "L002",
        "city": "Los Angeles",
        "latitude": 34.052235,
        "longitude": -118.243683,
        "compartments": {"small": 25, "medium": 10, "large": 8}
    }

@pytest.fixture()
def parcel_1() -> Parcel:
    return Parcel(
        parcel_id="P12345",
        height=30,
        length=50,
        weight=5
    )

@pytest.fixture()
def parcel_1_data() -> ParcelsDataDict:
    return {
        "parcel_id": "P12345",
        "height": 30,
        "length": 50,
        "weight": 5
    }

@pytest.fixture()
def parcel_2() -> Parcel:
    return Parcel(
        parcel_id="P67890",
        height=20,
        length=40,
        weight=3
    )

@pytest.fixture()
def parcel_2_data() -> ParcelsDataDict:
    return {
        "parcel_id": "P67890",
        "height": 20,
        "length": 40,
        "weight": 3
    }

@pytest.fixture()
def deliver_1() -> Deliver:
    return Deliver(
        parcel_id="P12345",
        locker_id="L001",
        sender_email="john.doe@example.com",
        receiver_email="jane.smith@example.com",
        sent_date="2023-12-01",
        expected_delivery_date="2023-12-05"
    )

@pytest.fixture()
def deliver_1_data() -> DeliversDataDict:
    return {
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "john.doe@example.com",
        "receiver_email": "jane.smith@example.com",
        "sent_date": "2023-12-01",
        "expected_delivery_date": "2023-12-05"
    }

@pytest.fixture()
def deliver_2() -> Deliver:
    return Deliver(
        parcel_id="P67890",
        locker_id="L002",
        sender_email="jane.smith@example.com",
        receiver_email="john.doe@example.com",
        sent_date="2023-12-02",
        expected_delivery_date="2023-12-06"
    )

@pytest.fixture()
def deliver_2_data() -> DeliversDataDict:
    return {
        "parcel_id": "P67890",
        "locker_id": "L002",
        "sender_email": "jane.smith@example.com",
        "receiver_email": "john.doe@example.com",
        "sent_date": "2023-12-02",
        "expected_delivery_date": "2023-12-06"
    }