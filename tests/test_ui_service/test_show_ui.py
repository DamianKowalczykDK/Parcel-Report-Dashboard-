from unittest.mock import MagicMock, patch
from src.ui_service import UiService


@patch("src.ui_service.UiService._send_parcel")
@patch("src.ui_service.st")
def test_show_ui_send_order(mock_st: MagicMock, mock_send: MagicMock, mock_ui_service: UiService) -> None:

    mock_st.sidebar.radio.return_value = "Send Order"
    mock_st.button.return_value = True
    mock_ui_service.show_ui()
    mock_send.assert_called_once()

@patch("src.ui_service.UiService._find_parcel")
@patch("src.ui_service.st")
def test_show_ui_find_order(mock_st: MagicMock, mock_find: MagicMock , mock_ui_service: UiService) -> None:
    mock_st.sidebar.radio.return_value = "Track your shipment"
    mock_st.button.return_value = True

    mock_ui_service.show_ui()
    mock_find.assert_called_once()

@patch("src.report_service.ReportService.report_most_common_parcel_sizes_per_locker")
@patch("src.ui_service.st")
def test_show_ui_report(mock_st: MagicMock, mock_report: MagicMock, mock_ui_service: UiService) -> None:
    mock_st.sidebar.radio.return_value = "Report"
    mock_st.button.return_value = True

    mock_ui_service.show_ui()
    mock_report.assert_called_once()





