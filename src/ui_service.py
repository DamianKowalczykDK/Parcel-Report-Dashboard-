from src.file_service import DeliverReaderJson, DeliverWriterJson
from src.validator import DeliversDataDictValidator
from src.model import DeliversDataDict, Deliver
from src.report_service import ReportService
from dataclasses import dataclass, field
from datetime import datetime, date
from collections import defaultdict
import streamlit as st
from typing import cast
import json


@dataclass
class UiService:
    """
    User Interface service implemented with Streamlit for managing parcel deliveries.

    This class provides UI components and logic to:
    - Send new parcel delivery data (_send)
    - Find and track existing parcel deliveries (_find)
    - Display reports based on parcel delivery data (show_ui)

    Attributes:
        report_service (ReportService): Service object providing parcel report data and methods.
        validator (DeliversDataDictValidator): Validator to verify the structure and correctness of delivery data.

    Methods:
        _send(file_path: str) -> DeliversDataDict | None:
            Presents input fields for parcel delivery details and saves validated data to a JSON file.

        _find(file_path: str) -> None:
            Allows searching for a parcel by its ID and displays delivery status.

        show_ui() -> None:
            Displays the main Streamlit UI with a sidebar menu to choose between sending orders,
            tracking shipments, or viewing reports. Fetches report data and shows it as dataframes.
    """

    report_service: ReportService
    validator: DeliversDataDictValidator = field(default_factory=DeliversDataDictValidator)

    def _send_parcel(self, file_path: str) -> DeliversDataDict | None:
        """
        Presents a form in Streamlit for entering new shipping details and saves the data to a JSON file.

        The form collects shipment number, locker number, sender and receiver emails, send date, and expected delivery date.
        It validates the input data, appends the new delivery to existing records, and writes back to the JSON file.
        Displays success or error messages based on the operation result.

        Args:
            file_path (str): Path to the JSON file where delivery data is stored.

        Returns:
            DeliversDataDict | None: Returns the new delivery data dictionary if successfully saved; otherwise, None.
        """

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

            if not self.validator.validate(new_delivery):
                st.error("Data did not pass validation. Please check dates and email address.")
                return None

            reader = DeliverReaderJson()
            existing_data = reader.read(file_path)
            existing_data.append(cast(Deliver, new_delivery))

            try:
                writer = DeliverWriterJson()
                writer.write(file_path, existing_data)
                st.success("Your package has been shipped")
                st.json(new_delivery)
                return new_delivery

            except Exception as e:
                st.error(f"Data could not be written to file: {e}")

        return None

    def _find_parcel(self, file_path: str) -> None:
        """
            Allows the user to search for a parcel by ID from a JSON file and displays delivery status using Streamlit.

            This function:
            - Loads parcel data from the given JSON file.
            - Validates the data structure of each parcel using DeliversDataDictValidator.
            - Prompts the user to input a parcel ID via a Streamlit text input.
            - Displays appropriate messages based on whether the parcel is found, its expected delivery date,
              and whether it is ready for pickup or still out for delivery.

            Args:
                file_path (str): Path to the JSON file containing parcel delivery data.

            Returns:
                None
            """

        with open(file_path, "r", encoding="utf8") as file:
            data = json.load(file)

        if not all(self.validator.validate(parcel) for parcel in data) :
            st.error("Invalid data structure in JSON file.")
            return

        st.subheader("Find Parcel 🔍")
        page = st.text_input("Enter the number ID")
        result = defaultdict(list)
        if page:
            for parcel in data:
                if parcel["parcel_id"] == page:
                    result[parcel["parcel_id"]].append(parcel)

            if not result:
                st.write("Not found parcel")


        for key, value  in result.items():
            for parcel in value:
                expected_delivery = datetime.strptime(parcel["expected_delivery_date"], "%Y-%m-%d").date()
                if expected_delivery < date.today():
                    if st.button("Parcel is ready for pickup. You can collect your parcel now"):
                        st.success(f"Parcel number {parcel["parcel_id"]} has been picked up")
                else:
                    st.write(f"Parcel number {parcel["parcel_id"]} out for delivery, estimated delivery time"
                             f"  {parcel["expected_delivery_date"]}")

    def show_ui(self) -> None:
        """
        Displays the main user interface of the parcel delivery monitor using Streamlit.

        Provides a sidebar menu to navigate between:
        - Sending a new order
        - Tracking an existing shipment
        - Viewing various parcel reports

        Based on user selection, calls the corresponding private methods to handle input, display data,
        or show reports as interactive Streamlit tables.

        Returns:
            None
        """
        st.title("Automated Parcel Delivery Monitor 📦")
        st.sidebar.title("Menu")
        page = st.sidebar.radio("Select", ["Send Order", "Track your shipment", "Report"])

        match page:
            case "Send Order":
                self._send_parcel("data_json/delivers.json")
            case "Track your shipment":
                self._find_parcel("data_json/delivers.json")
            case "Report":
                st.subheader("Reports")
                if st.button("📊 Most Common Parcel Sizes per Locker"):
                    df = self.report_service.report_most_common_parcel_sizes_per_locker()
                    st.dataframe(df)
                if st.button('📊 City Most Shipments by Size'):
                    df = self.report_service.report_city_most_shipments_by_size()
                    st.dataframe(df)
                if st.button("📊 Max days between sent and expected date"):
                    df = self.report_service.report_max_days_between_sent_and_expected()
                    st.dataframe(df)
                if st.button("📊 is parcel limit in locker exceeded"):
                    df = self.report_service.report_is_parcel_limit_in_locker_exceeded()
                    st.dataframe(df)
