from locker_streamlit.report import (
    report_most_common_parcel_sizes_per_locker,
    report_city_most_shipments_by_size
)
from unittest.mock import MagicMock, patch


@patch("locker_streamlit.report.st")
def test_report_most_common_parcel_sizes_per_locker(mock_service: MagicMock) -> None:

    mock_service.most_common_parcel_sizes_per_locker.return_value = {
        "L001": ["SMALL", "MEDIUM"],
        "L002": ["LARGE"]
    }

    report_most_common_parcel_sizes_per_locker(mock_service)

@patch("locker_streamlit.report.st")
def test_report_city_most_shipments_by_size(mock_service: MagicMock) -> None:

    mock_service.city_most_shipments_by_size.return_value =  {
            "sent": {"CompartmentsLarge.SMALL": "Chicago"},
            "received": {"CompartmentsLarge.SMALL": "New York"}
    }

    report_city_most_shipments_by_size(mock_service)


