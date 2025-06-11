from logging import raiseExceptions
from unittest.mock import patch, MagicMock
from datetime import date, timedelta

import pytest
from pyexpat.errors import messages

from locker_streamlit.send_parcel import send
from src.file_service import DeliverWriterJson


@patch('locker_streamlit.send_parcel.st')
def test_send_parcel_successfully(mock_st: MagicMock) -> None:
    mock_st.text_input.side_effect = ['1234', 'L001', 'abc@gmail.com', 'bcd@gmail.com']
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True

    entry = send('data_json/delivers.json')

    assert isinstance(entry, dict)


@patch('locker_streamlit.send_parcel.st')
def test_send_parcel_no_data(mock_st: MagicMock) -> None:
    mock_st.text_input.side_effect = ['12345', '', 'abc@gmail.com', 'bcd@gmail.com']
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]

    entry = send('data_json/delivers.json')

    assert entry is None
    mock_st.error.assert_called_once_with('Please fill out all fields')

@patch('locker_streamlit.send_parcel.st')
def test_send_parcel_no_validate(mock_st: MagicMock) -> None:
    mock_st.text_input.side_effect = ['12345', 'L001', 'abc.gmail.pl', 'bcd@gmail.com']
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]

    entry = send('data_json/delivers.json')

    assert entry is None
    mock_st.error.assert_called_once_with('Data did not pass validation. Please check dates and email address.')

@patch('locker_streamlit.send_parcel.DeliverWriterJson.write')
@patch('locker_streamlit.send_parcel.st')
def test_send_parcel_exception(mock_st: MagicMock, mock_write: MagicMock, caplog: pytest.LogCaptureFixture) -> None:
    mock_st.text_input.side_effect = ['1234', 'L001', 'abc@gmail.com', 'bcd@gmail.com']
    mock_st.date_input.side_effect = [date.today(), date.today() + timedelta(days=1)]
    mock_st.button.return_value = True

    mock_write.side_effect = Exception()

    send('data_json/delivers.json')
    mock_st.error.assert_called_once()
    mock_st.error.assert_called_once_with(f'Data could not be written to file: ')


