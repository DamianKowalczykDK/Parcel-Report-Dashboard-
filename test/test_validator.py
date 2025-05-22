from src.validator import (
    Validator,
    UserDataDictValidator,
    LockerDataDictValidator,
    ParcelDataDictValidator,
    DeliversDataDictValidator
)
from src.model import UsersDataDict, LockersDataDict, ParcelsDataDict, User, DeliversDataDict
import pytest

from test.conftest import fake_user


@pytest.mark.parametrize("value, expected", [
    (0, False),
    (5, True),
    ("5", True),
    (-1, False),
    ("-1", False),
    ("abc", False),
])
def test_is_positive(value: int | str, expected: bool) -> None:
    assert Validator.is_positive(value) == expected


@pytest.mark.parametrize("email, expected", [
    ("valid@gmail.com", True),
    ("valid@example.com", False),
    ("invalid-email.com", False),
    ("@missingusername.com", False),
    ("missingdomain@", False),
    ("user@nonexistentdomain.invalid", False)
])
def test_is_valid_email(email: str, expected: bool) -> None:
    assert Validator.is_valid_email(email) == expected


@pytest.mark.parametrize("data, expected", [
    ({
        "email": "john.doe@example.com",
        "surname": "Doe",
        "city": "New York",
        "latitude": 40.712776,
        "longitude": -74.005974
    }, False),
    ({
        "email": "jane.smith@gmail.com",
        "name": "Jane",
        "surname": "Smith",
        "city": "Los Angeles",
        "latitude": 34.052235,
        "longitude": -118.243683
    }, True),

    (fake_user(), False),
    ])

def test_has_required_keys(data: UsersDataDict | User, expected: bool) -> None:
    assert Validator.has_required_keys(data, ["name"]) == expected


@pytest.mark.parametrize("data, expected", [
    ({"email": "jane.smith@gmail.com"}, True),
    ({"email": "jane.smith.gmail.com"}, False),

])
def test_user_data_dict_validator(data: UsersDataDict, expected: bool) -> None:
    validate = UserDataDictValidator(required_keys=["email"])
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"email": "john.doe@example.com", "name": "John","surname": "Doe", "city": "New York","latitude": 40.712776}, False),
    ({"name": "John","surname": "Doe", "city": "New York","latitude": 40.712776, "longitude": -74.005974}, False)

])
def test_user_data_dict_validator_missing_key(data: UsersDataDict, expected: bool) -> None:
    validate = UserDataDictValidator()
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"locker_id": "L001","city": "New York","latitude": 40.730610,"longitude": -73.935242,"compartments": {"small": 20,"medium": 15,"large": 5}}, True),
    ({"locker_id": "L001","city": "New York","latitude": 40.730610,"longitude": -73.935242}, False),
    ({"locker_id": "L001","city": "New York","latitude": 40.730610,"compartments": {"small": 20,"medium": 15,"large": 5}}, False),

])
def test_locker_data_dict_validator_missing_key(data: LockersDataDict, expected: bool) -> None:
    validate = LockerDataDictValidator()
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"compartments": {"small": 20,"medium": 15,"large": 5}}, True),
    ({"compartments": {"small": 20,"medium": 15,"large": -1}}, False),
    ({"compartments": "small"}, False)

])
def test_locker_data_dict_validator(data: LockersDataDict, expected: bool) -> None:
    validate = LockerDataDictValidator(required_keys=["compartments"])
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"parcel_id": "P12345", "height": 30,"length": 50,"weight": 5}, True),
    ({"parcel_id": "P12345", "height": 30,"length": 50,}, False),
    ({"parcel_id": "P12345", "height": 30, "weight": 5}, False),
    ({"parcel_id": "P12345", "length": 50,"weight": 5}, False),
    ({"height": 30,"length": 50,"weight": 5}, False),
])
def test_parcel_data_dict_validator_missing_key(data: ParcelsDataDict, expected: bool) -> None:
    validate = ParcelDataDictValidator()
    assert validate.validate(data) == expected


@pytest.mark.parametrize("data, expected", [
    ({"height": -1, "length": 1, "weight": 1}, False),
    ({"height": 1, "length": -1, "weight": 1}, False),
    ({"height": 1, "length": 1, "weight": -1}, False)
])
def test_parcel_data_dict_validator(data: ParcelsDataDict, expected: bool) -> None:
    validate = ParcelDataDictValidator(required_keys=["height", "length", "weight"])
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "alice.smith@example.com",
        "receiver_email": "john.doe@example.com",
        "sent_date": "2023-12-01",
        "expected_delivery_date": "2023-12-05"
    },True),
({
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "alice.smith@example.com",
        "sent_date": "2023-12-01",
        "expected_delivery_date": "2023-12-05"
    },False),
({
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "alice.smith@example.com",
        "receiver_email": "john.doe@example.com",
        "sent_date": "2023-12-01",
    },False),

])
def test_deliver_data_dict_validator_missing_key(data: DeliversDataDict, expected: bool) -> None:
    validate = DeliversDataDictValidator()
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({"sender_email": "alice.smith@example.com", "receiver_email": "alice.smith@example.com"}, False),
])
def test_deliver_data_dict_validator_sender_email(data: DeliversDataDict, expected: bool) -> None:
    validate = DeliversDataDictValidator(required_keys=["sender_email", "receiver_email"])
    assert validate.validate(data) == expected

@pytest.mark.parametrize("data, expected", [
    ({
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "alice.smith@example.com",
        "receiver_email": "john.doe@example.com",
        "sent_date": "2023-12-10",
        "expected_delivery_date": "2023-12-05"
    },False),
({
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "alice.smith@example.com",
        "receiver_email": "alice.smith@example.com",
        "sent_date": "10-10-2020",
        "expected_delivery_date": "20-2020-10"
    },False),

])
def test_deliver_data_dict_validator_sent_date_and_expected_delivery_date(
        data: DeliversDataDict,
        expected: bool) -> None:
    validate = DeliversDataDictValidator()
    assert validate.validate(data) == expected