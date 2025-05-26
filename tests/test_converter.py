from src.converter import UserConverter, LockerConverter, ParcelConverter, DeliverConverter
from pytest import FixtureRequest
import pytest



@pytest.mark.parametrize("user_data_fixture, expected_user_fixture", [
    ("user_1_data", "user_1" ),
])
def test_convert_user_from_dict(user_data_fixture: str, expected_user_fixture: str, request: FixtureRequest) -> None:
    user = request.getfixturevalue(expected_user_fixture)
    user_data = request.getfixturevalue(user_data_fixture)
    converter = UserConverter()
    result = converter.convert(user_data)
    assert result == user

@pytest.mark.parametrize("locker_data_fixture, expected_locker_fixture", [
    ("locker_1_data", "locker_1" ),
])
def test_convert_locker_from_dict(locker_data_fixture: str, expected_locker_fixture: str, request: FixtureRequest) -> None:
    locker = request.getfixturevalue(expected_locker_fixture)
    locker_data = request.getfixturevalue(locker_data_fixture)
    converter = LockerConverter()
    result = converter.convert(locker_data)
    assert result == locker

@pytest.mark.parametrize("parcel_data_fixture, expected_parcel_fixture", [
    ("parcel_1_data", "parcel_1" ),
    ("parcel_2_data", "parcel_2" ),
])
def test_converter_parcel_from_dict(parcel_data_fixture: str, expected_parcel_fixture: str, request: FixtureRequest) -> None:
    parcel = request.getfixturevalue(expected_parcel_fixture)
    parcel_data = request.getfixturevalue(parcel_data_fixture)
    converter = ParcelConverter()
    result = converter.convert(parcel_data)
    assert result == parcel

@pytest.mark.parametrize("deliver_data_fixture, expected_deliver_fixture", [
    ("deliver_1_data", "deliver_1" ),
    ("deliver_2_data", "deliver_2" ),
])
def test_converter_delivery_from_dict(deliver_data_fixture: str, expected_deliver_fixture: str, request: FixtureRequest) -> None:
    deliver = request.getfixturevalue(expected_deliver_fixture)
    deliver_data = request.getfixturevalue(deliver_data_fixture)
    converter = DeliverConverter()
    result = converter.convert(deliver_data)
    assert result == deliver