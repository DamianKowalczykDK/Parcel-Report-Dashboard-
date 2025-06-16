from unittest.mock import patch, MagicMock
from datetime import date, timedelta


from locker_streamlit.send_parcel import send

@patch("locker_streamlit.send_parcel.DeliverWriterJson.write")
@patch("locker_streamlit.send_parcel.DeliverReaderJson.read")
@patch("locker_streamlit.send_parcel.st")
def test_send_parcel_successfully(mock_st: MagicMock, mock_read: MagicMock, mock_write: MagicMock) -> None:
    mock_st.text_input.side_effect = ["1234", "L001", "abc@gmail.com", "bcd@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True

    mock_read.return_value = []

    send("fake_path.json")

    mock_st.success.assert_called_once_with("Your package has been shipped")
    mock_write.assert_called()

@patch("locker_streamlit.send_parcel.DeliverWriterJson.write")
@patch("locker_streamlit.send_parcel.st")
def test_send_parcel_no_data(mock_st: MagicMock, mock_write: MagicMock) -> None:
    mock_st.text_input.side_effect = ["12345", "", "abc@gmail.com", "bcd@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]

    entry = send(f"fake_path.json")

    assert entry is None
    mock_st.error.assert_called_once_with("Please fill out all fields")
    mock_write.assert_not_called()

@patch("locker_streamlit.send_parcel.DeliverWriterJson.write")
@patch("locker_streamlit.send_parcel.st")
def test_send_parcel_no_validate(mock_st: MagicMock, mock_write: MagicMock) -> None:
    mock_st.text_input.side_effect = ["12345", "L001", "abc.gmail.pl", "bcd@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]

    entry = send("fake_path.json")

    assert entry is None
    mock_st.error.assert_called_once_with("Data did not pass validation. Please check dates and email address.")
    mock_write.assert_not_called()


@patch("locker_streamlit.send_parcel.DeliverWriterJson.write")
@patch("locker_streamlit.send_parcel.DeliverReaderJson.read")
@patch("locker_streamlit.send_parcel.st")
def test_send_parcel_exception(mock_st: MagicMock, mock_read: MagicMock, mock_write: MagicMock) -> None:
    mock_st.text_input.side_effect = ["1234", "L001", "abc@gmail.com", "bcd@gmail.com"]
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True

    mock_read.return_value = []
    mock_write.side_effect = Exception()

    send("fake_path.json")
    mock_st.error.assert_called_once()
    mock_st.error.assert_called_once_with(f"Data could not be written to file: ")


