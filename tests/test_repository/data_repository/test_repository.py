from tests.test_repository.data_repository.conftest import user_data_repository
from src.repository import UserDataRepository
from src.model import UsersDataDict, User
from unittest.mock import MagicMock
import logging
import pytest


def test_get_data_empty_cache_logs_warning(user_data_repository: UserDataRepository, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        data = user_data_repository.get_data()
    assert len(data) == 0
    assert len(caplog.records) == 1

def test_process_data(
        user_data_repository: UserDataRepository,
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock,
        user_1_data: UsersDataDict,
        user_1: User
    ) -> None:
    file_reader_mock.read.return_value = user_1_data
    validator_mock.validate.return_value = True
    converter_mock.convert.return_value = user_1

    data = user_data_repository.refresh_data()
    file_reader_mock.read.assert_called_with("user.json")
    assert file_reader_mock.read.call_count == 2
    assert data[0] == user_1


def test_no_filename_raises_value_error(
        file_reader_mock: MagicMock,
        validator_mock: MagicMock,
        converter_mock: MagicMock) -> None:

    with pytest.raises(ValueError, match='No filename set'):
        _ = UserDataRepository(
            file_reader=file_reader_mock,
            validator=validator_mock,
            converter=converter_mock,
            filename=None
        )

def test_no_invalid_entry_logs_error(user_data_repository: UserDataRepository,file_reader_mock, validator_mock, caplog) -> None:
    file_reader_mock.read.return_value =[
    {
    "email": "alice.smith@gmail.com",
    "name": "Alice",
    "surname": "Smith",
    "city": "Chicago",
    "latitude": 41.878113,
    "longitude": -87.629799
     },
    {
        "email": "alice.smith@gmail.com",
        "name": "Alice",
        "surname": "Smith",
        "city": "Chicago",
    },
    ]

    validator_mock.validate.side_effect = [True, False]

    with caplog.at_level(logging.ERROR):
        data = user_data_repository.refresh_data()

    assert "Invalid entry: {'email': 'alice.smith@gmail.com', 'name': 'Alice', 'surname': 'Smith', 'city': 'Chicago'}" in caplog.text
    assert len(data) == 1
