from tests.test_service.conftest import delivers_list, users_list, parcels_list
from src.model import Deliver, User, Parcel, Locker
from src.service import ParcelReportService
from unittest.mock import MagicMock


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