from src.validator import DeliversDataDictValidator
from collections import defaultdict
from datetime import date, datetime
import streamlit as st
import json

def find(file_path: str) -> None:
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

    validator = DeliversDataDictValidator()

    with open(file_path, "r", encoding="utf8") as file:
        data = json.load(file)

    if not all(validator.validate(parcel) for parcel in data) :
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

