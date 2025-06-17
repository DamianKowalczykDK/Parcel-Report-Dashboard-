from locker_streamlit.report import (
    report_most_common_parcel_sizes_per_locker,
    report_city_most_shipments_by_size,
    report_max_days_between_sent_and_expected,
    report_is_parcel_limit_in_locker_exceeded
)
from unittest.mock import MagicMock


def test_report_most_common_parcel_sizes_per_locker() -> None:
    mock_service = MagicMock()
    mock_service.most_common_parcel_sizes_per_locker.return_value = {
        "L001": ["SMALL", "MEDIUM"],
        "L002": ["LARGE"]
    }

    report_most_common_parcel_sizes_per_locker(mock_service)


def test_report_city_most_shipments_by_size() -> None:
    mock_service = MagicMock()
    mock_service.city_most_shipments_by_size.return_value =  {
            "sent": {"CompartmentsLarge.SMALL": "Chicago"},
            "received": {"CompartmentsLarge.SMALL": "New York"}
    }

    report_city_most_shipments_by_size(mock_service)


def test_report_max_days_between_sent_and_expected() -> None:
    mock_service = MagicMock()
    mock_service.max_days_between_sent_and_expected.return_value = {
        "alice.smith@gmail.com": 13
    }

    report_max_days_between_sent_and_expected(mock_service)


def test_report_is_parcel_limit_in_locker_exceeded() -> None:
    mock_service = MagicMock()
    mock_service.is_parcel_limit_in_locker_exceeded.return_value = {
        "L001": {"small": 9, "medium": 9, "large": 5},
        "L002": {"small": 24,"medium": 10, "large": 8}
    }

    report_is_parcel_limit_in_locker_exceeded(mock_service)
