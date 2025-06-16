from src.file_service import DeliverReaderJson, DeliverWriterJson
from src.validator import DeliversDataDictValidator
from src.model import DeliversDataDict, Deliver
from datetime import date
from typing import cast
import streamlit as st


def send(file_path: str) -> DeliversDataDict | None:
    """
    Collects delivery details from the user via Streamlit form, validates them,
    and saves the data_json to a JSON file.

    Args:
        file_path (str): The path to the JSON file where the delivery data_json should be saved.

    Returns:
        DeliversDataDict | None: The new delivery data_json if successfully submitted and saved, else None.
    """
    validator = DeliversDataDictValidator()

    st.subheader("Enter shipping details")

    parcel_id = st.text_input("Please provide your shipment number")
    locker_id = st.text_input("Enter the parcel locker number")
    sender_email = st.text_input("Sender email")
    receiver_email = st.text_input("Receiver email")
    sent_date = st.date_input("Select send date", value=date.today())
    expected_delivery_date = st.date_input("Select expected delivery date", value=date.today())

    if st.button("Submit"):
        if not all([
            parcel_id,
            locker_id,
            sender_email,
            receiver_email,
            sent_date,
            expected_delivery_date
        ]):
            st.error("Please fill out all fields")
            return None

        new_delivery: DeliversDataDict = {
            "parcel_id": parcel_id,
            "locker_id": locker_id,
            "sender_email": sender_email,
            "receiver_email": receiver_email,
            "sent_date": sent_date.strftime("%Y-%m-%d"),
            "expected_delivery_date": expected_delivery_date.strftime("%Y-%m-%d")
        }

        if not validator.validate(new_delivery):
            st.error("Data did not pass validation. Please check dates and email address.")
            return None

        existing_data = DeliverReaderJson.read(file_path)
        existing_data.append(cast(Deliver, new_delivery))

        try:
            DeliverWriterJson.write(file_path, existing_data)
            st.success("Your package has been shipped")
            st.json(new_delivery)
            return new_delivery

        except Exception as e:
            st.error(f"Data could not be written to file: {e}")

    return None


