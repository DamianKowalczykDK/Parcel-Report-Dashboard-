from src.report_service import ReportService
from unittest.mock import MagicMock
import pandas as pd

def test_report_most_common_parcel_sizes_per_locker(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.most_common_parcel_sizes_per_locker.return_value = {
        "L001": ["SMALL", "MEDIUM"],
        "L002": ["LARGE"]
    }

    result = mock_report_service.report_most_common_parcel_sizes_per_locker()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_report_city_most_shipments_by_size(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.city_most_shipments_by_size.return_value = {
        "sent": {"small": "Chicago"},
        "received": {"small": "New York"}
    }
    result = mock_report_service.report_city_most_shipments_by_size()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2

def test_report_max_days_between_sent_and_expected(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.max_days_between_sent_and_expected.return_value = {
        "alice.smith@gmail.com": 13
    }

    result = mock_report_service.report_max_days_between_sent_and_expected()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1

def test_report_is_parcel_limit_in_locker_exceeded(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.is_parcel_limit_exceeded.return_value = {
        "LOO1": {"small": 9, "medium": 9, "large": 9},
        "LOO2": {"small": 19, "medium": 19, "large": 5},
    }

    result = mock_report_service.report_is_parcel_limit_in_locker_exceeded()
    assert isinstance(result, pd.DataFrame)

