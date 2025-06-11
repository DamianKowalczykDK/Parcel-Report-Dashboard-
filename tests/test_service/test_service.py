import pytest

from tests.conftest import parcel_1
from tests.test_service.conftest import delivers_list, users_list, parcels_list
from src.model import Deliver, User, Parcel, Locker, CompartmentsLarge
from src.service import ParcelReportService
from unittest.mock import MagicMock
import logging

def test_city_most_shipments_by_size(
        service: ParcelReportService,
        mock_repository: MagicMock,
        delivers_list: list[Deliver],
        users_list: list[User],
        parcels_list: list[Parcel]) -> None:

    mock_repository.delivery_repo.get_data.return_value = delivers_list
    mock_repository.user_repo.get_data.return_value = users_list
    mock_repository.parcel_repo.get_data.return_value = parcels_list

    result = service.city_most_shipments_by_size()

    expected = {
        'sent': {'CompartmentsLarge.MEDIUM': 'New York', 'CompartmentsLarge.SMALL': 'Los Angeles'},
        'received': {'CompartmentsLarge.MEDIUM': 'Los Angeles', 'CompartmentsLarge.SMALL': 'New York'}
    }

    assert expected == result

def test_most_common_parcel_sizes_per_locker(
        service: ParcelReportService,
        mock_repository: MagicMock,
        delivers_list: list[Deliver],
        users_list: list[User],
        parcels_list: list[Parcel],
        lockers_list: list[Locker]) -> None:

    mock_repository.delivery_repo.get_data.return_value = delivers_list
    mock_repository.user_repo.get_data.return_value = users_list
    mock_repository.parcel_repo.get_data.return_value = parcels_list
    mock_repository.locker_repo.get_data.return_value = lockers_list


    result = service.most_common_parcel_sizes_per_locker()

    expected = {
         'L001': ['medium'],
         'L002': ['small']
    }
    assert expected == result

def test_max_days_between_sent_and_expected_deliver_with_single_sender(
        service: ParcelReportService,
        mock_repository: MagicMock,
        deliver_1: MagicMock) -> None:

    mock_repository.delivery_repo.get_data.return_value = [deliver_1]

    result = service.max_days_between_sent_and_expected()

    expected = {
        "john.doe@example.com": 4
    }
    assert expected == result

def test_max_days_between_sent_and_expected_deliver_with_multiple_senders(
        service: ParcelReportService,
        mock_repository: MagicMock,
        deliver_1: MagicMock,
        deliver_2: MagicMock) -> None:

    mock_repository.delivery_repo.get_data.return_value = [deliver_1, deliver_2]

    result = service.max_days_between_sent_and_expected()

    expected = {
        "john.doe@example.com": 4,
        "jane.smith@example.com": 4
    }
    assert expected == result

def test_is_parcel_limit_in_locker_exceeded_no_places_available(
        service: ParcelReportService,
        mock_repository: MagicMock,
        locker_1: Locker,
        parcel_1: Parcel,
        deliver_1: Deliver) -> None:

    mock_repository.locker_repo.get_data.return_value = [locker_1]
    mock_repository.parcel_repo.get_data.return_value = [parcel_1]
    mock_repository.delivery_repo.get_data.return_value = [deliver_1]

    result = service.is_parcel_limit_in_locker_exceeded()

    expected = {
        "L001": {CompartmentsLarge.SMALL :20, CompartmentsLarge.MEDIUM: 14, CompartmentsLarge.LARGE: 5}
    }

    assert result == expected

def test_test_is_parcel_limit_in_locker_exceeded_no_places_available_with_logs_warning(
        service: ParcelReportService,
        mock_repository: MagicMock,
        parcel_1: Parcel,
        deliver_1: Deliver,
        caplog: pytest.LogCaptureFixture) -> None:

    mock_repository.locker_repo.get_data.return_value = [Locker(
        locker_id="L001",
        city="New York",
        latitude=40.730610,
        longitude=-73.935242,
        compartments= {CompartmentsLarge.SMALL: 20, CompartmentsLarge.MEDIUM: 0, CompartmentsLarge.LARGE: 5}
    )]
    mock_repository.parcel_repo.get_data.return_value = [parcel_1]
    mock_repository.delivery_repo.get_data.return_value = [deliver_1]

    with caplog.at_level(logging.WARNING):
        data = service.is_parcel_limit_in_locker_exceeded()

    assert len(data) == 1
    assert any('No places available' in record.message for record in caplog.records)
