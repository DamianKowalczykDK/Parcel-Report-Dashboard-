from src.service import ParcelReportService
import streamlit as st
import pandas as pd


def report_most_common_parcel_sizes_per_locker(service: ParcelReportService) -> None:
    """
    Displays a table of the most common parcel sizes per locker using Streamlit.

    Calls the `most_common_parcel_sizes_per_locker` method from the provided service to get data
    and presents it as a Streamlit table with columns for locker ID and the corresponding
    most frequent parcel sizes.

    Args:
        service (ParcelReportService): A service object that provides parcel report data.

    Returns:
        None
    """
    data = service.most_common_parcel_sizes_per_locker()

    df = pd.DataFrame([
        {"Locker ID": locker_id, "Most Common Size(s)": " ".join(sizes)} for locker_id, sizes in data.items()])

    st.table(df)

def report_city_most_shipments_by_size(service: ParcelReportService) -> None:
    """
    Displays a table of cities with the most shipments sent and received, grouped by parcel size.

    Calls the `city_most_shipments_by_size` method from the provided service to get data
    and presents it as a Streamlit table with columns indicating the parcel size and the corresponding
    city with the most activity for sending or receiving.

    Args:
        service (ParcelReportService): A service object that provides parcel shipment statistics.

    Returns:
        None
    """
    data = service.city_most_shipments_by_size()

    df = pd.DataFrame([{"size/city": size, "sent/recevied": city} for city, size in data.items()])

    st.table(df)


