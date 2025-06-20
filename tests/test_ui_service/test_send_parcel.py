from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from src.ui_service import UiService

@patch("src.ui_service.DeliverWriterJson.write")
@patch("src.ui_service.DeliverReaderJson.read")
@patch("src.ui_service.st")
def test_ui_service_if_send_successful(
        mock_st: MagicMock,
        mock_load: MagicMock,
        mock_write: MagicMock,
        mock_ui_service: UiService) -> None:

    mock_st.text_input.side_effect = ["P1234", "L001", "jon.doe@gmail.com", "jane.doe@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True
    mock_load.return_value = []
    result = mock_ui_service._send_parcel("fake_path.json")

    assert result is not None
    assert result["parcel_id"] == "P1234"
    assert result["locker_id"] == "L001"
    assert result["sender_email"] == "jon.doe@gmail.com"
    assert result["receiver_email"] == "jane.doe@gmail.com"

    mock_st.success.assert_called_once_with("Your package has been shipped")
    mock_write.assert_called()

@patch("src.ui_service.DeliverWriterJson.write")
@patch("src.ui_service.st")
def test_ui_service_if_send_has_no_all_data(
        mock_st: MagicMock,
        mock_write: MagicMock,
        mock_ui_service: UiService)-> None:

    mock_st.text_input.side_effect = ["P1234", "L001", "", "jon.doe@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True

    result = mock_ui_service._send_parcel("fake_path.json")

    assert result is None
    mock_st.error.assert_called_once_with("Please fill out all fields")
    mock_write.assert_not_called()

@patch("src.ui_service.DeliverWriterJson.write")
@patch("src.ui_service.st")
def test_ui_service_if_send_has_not_validate(
        mock_st: MagicMock,
        mock_write: MagicMock,
        mock_ui_service: UiService) -> None:

    mock_st.text_input.side_effect = ["P1234", "L001", "jon.doe@gmail.com", "bcd.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True

    mock_ui_service._send_parcel("fake_path.json")

    mock_st.error.assert_called_once_with("Data did not pass validation. Please check dates and email address.")
    mock_write.assert_not_called()

@patch("src.ui_service.DeliverWriterJson.write")
@patch("src.ui_service.DeliverReaderJson.read")
@patch("src.ui_service.st")
def test_ui_service_if_send_has_error_exception(
        mock_st: MagicMock,
        mock_load: MagicMock,
        mock_write: MagicMock,
        mock_ui_service: UiService) -> None:

    mock_st.text_input.side_effect = ["P1234", "L001", "jon.doe@gmail.com", "jane.doe@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True
    mock_load.return_value = []

    mock_write.side_effect = Exception()

    mock_ui_service._send_parcel("fake_path.json")

    mock_st.error.assert_called_once_with("Data could not be written to file: ")
