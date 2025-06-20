from unittest.mock import MagicMock, patch
from datetime import date, timedelta

from src.model import DeliversDataDict
from src.ui_service import UiService


@patch("src.ui_service.open")
@patch("src.ui_service.json.load")
@patch("src.ui_service.st")
def test_ui_service_if_not_find_parcel(
        mock_st: MagicMock,
        mock_load: MagicMock,
        mock_open: MagicMock,
        deliver_3_data: DeliversDataDict,
        mock_ui_service: UiService) -> None:

    mock_open.return_value.__enter__.return_value = MagicMock()
    mock_load.return_value = [deliver_3_data]

    mock_st.text_input.return_value = "P123"
    mock_ui_service._find_parcel("fake_path.json")
    mock_st.write.assert_called_once_with("Not found parcel")


@patch("src.ui_service.open")
@patch("src.ui_service.json.load")
@patch("src.ui_service.st")
def test_ui_service_if_not_all_data(
        mock_st: MagicMock,
        mock_load: MagicMock,
        mock_open: MagicMock,
        mock_ui_service: UiService,
        deliver_1_data: DeliversDataDict) -> None:

    mock_open.return_value.__enter__.return_value = MagicMock()
    mock_load.return_value = [deliver_1_data]
    mock_st.text_input.return_value = "P12345"
    mock_st.button.return_value = True

    mock_ui_service._find_parcel("fake_path.json")

    mock_st.error.assert_called_once_with("Invalid data structure in JSON file.")


@patch("src.ui_service.open")
@patch("src.ui_service.json.load")
@patch("src.ui_service.st")
def test_ui_service_if_find_successful(
        mock_st: MagicMock,
        mock_load: MagicMock,
        mock_open: MagicMock,
        mock_ui_service: UiService,
        deliver_3_data: DeliversDataDict) -> None:

    mock_open.return_value.__enter__.return_value = MagicMock()

    mock_load.return_value = [deliver_3_data]

    mock_st.text_input.return_value = "P67890"
    mock_st.button.return_value = True

    mock_ui_service._find_parcel("fake_path.json")

    mock_st.success.assert_called_once_with("Parcel number P67890 has been picked up")


@patch("src.ui_service.open")
@patch("src.ui_service.json.load")
@patch("src.ui_service.st")
def test_ui_service_if_find_parcel_is_on_the_way(
        mock_st: MagicMock,
        mock_load: MagicMock,
        mock_open: MagicMock,
        mock_ui_service: UiService) -> None:


    mock_open.return_value.__enter__.return_value = MagicMock()
    mock_load.return_value = [
        {
            "parcel_id": "P12345",
            "locker_id": "L001",
            "sender_email": "alice.smith@gmail.com",
            "receiver_email": "john.doe@gmail.com",
            "sent_date": "2025-01-01",
            "expected_delivery_date": date.today().strftime("%Y-%m-%d"),
        }
    ]

    mock_st.text_input.return_value = "P12345"
    mock_st.button.return_value = True

    ui_service = UiService(report_service=MagicMock())
    ui_service._find_parcel("fake_path.json")

    mock_st.write(f"Parcel number P12345 out for delivery, estimated delivery time {date.today() + timedelta(days=1)}")