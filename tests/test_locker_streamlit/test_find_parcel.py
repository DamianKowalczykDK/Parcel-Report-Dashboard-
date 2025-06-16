from locker_streamlit.find_parcel import find
from unittest.mock import MagicMock, patch

@patch("locker_streamlit.find_parcel.open")
@patch("locker_streamlit.find_parcel.json.load")
@patch("locker_streamlit.find_parcel.st")
def test_find_parcel_not_found_parcel(mock_st: MagicMock, mock_load: MagicMock, mock_open: MagicMock) -> None:

    mock_open.return_value._enter_.return_value = MagicMock()
    mock_load.return_value = [
        {
        "parcel_id": "P12345",
        "locker_id": "L001",
        "sender_email": "alice.smith@gmail.com",
        "receiver_email": "john.doe@gmail.com",
        "sent_date": "2025-01-01",
        "expected_delivery_date": "2025-01-07"
        }
    ]

    mock_st.text_input.return_value = "P1234"
    mock_st.button.return_value = False
    find("fake_data.json")
    mock_st.write.assert_called_once_with("Not found parcel")

@patch("locker_streamlit.find_parcel.open")
@patch("locker_streamlit.find_parcel.json.load")
@patch("locker_streamlit.find_parcel.st")
def test_find_parcel_successful(mock_st: MagicMock, mock_load: MagicMock, mock_open: MagicMock) -> None:
    mock_open.return_value._enter_.return_value = MagicMock()

    mock_load.return_value = [
        {
            "parcel_id": "P12345",
            "locker_id": "L001",
            "sender_email": "alice.smith@gmail.com",
            "receiver_email": "john.doe@gmail.com",
            "sent_date": "2025-01-01",
            "expected_delivery_date": "2025-01-07"
        }
    ]
    mock_st.text_input.return_value = "P12345"
    mock_st.button.return_value = True
    find("fake_data.json")

@patch("locker_streamlit.find_parcel.open")
@patch("locker_streamlit.find_parcel.json.load")
@patch("locker_streamlit.find_parcel.st")
def test_find_parcel_estimated_delivery(mock_st: MagicMock, mock_load: MagicMock, mock_open: MagicMock) -> None:

    mock_open.return_value._enter_.return_value = MagicMock()
    mock_load.return_value = [
        {
            "parcel_id": "P12345",
            "locker_id": "L001",
            "sender_email": "alice.smith@gmail.com",
            "receiver_email": "john.doe@gmail.com",
            "sent_date": "2025-01-01",
            "expected_delivery_date": "2025-06-18"
        }
    ]
    mock_st.text_input.return_value = "P12345"
    mock_st.button.return_value = True
    find("fake_data.json")
    mock_st.write('Parcel number P12345 out for delivery, estimated delivery time 2025-06-18')

@patch("locker_streamlit.find_parcel.open")
@patch("locker_streamlit.find_parcel.json.load")
@patch("locker_streamlit.find_parcel.st")
def test_find_parcel_not_validate_data(mock_st: MagicMock, mock_load: MagicMock, mock_open: MagicMock) -> None:

    mock_open.return_value._enter_.return_value = MagicMock()
    mock_load.return_value = [
        {
            "parcel_id": "P12345",
            "locker_id": "L001",
            "sender_email": "alice.smith@gmail.com",
            "receiver_email": "john.doe",
            "sent_date": "2025-01-01",
            "expected_delivery_date": "2025-06-18"
        }
    ]

    mock_st.text_input.return_value = "P12345"
    mock_st.button.return_value = False
    find("fake_data.json")
    mock_st.error.assert_called_once_with("Invalid data structure in JSON file.")
