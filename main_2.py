from locker_streamlit import send_parcel
from src.repository import ParcelSummaryRepository
import streamlit as st

from locker_streamlit import find_parcel


def main1() -> None:
    st.title("Automated Parcel Delivery Monitor 📦")
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Select", ["Send Order", "Track your shipment", "Report"])
    if page == "Send Order":
        send_parcel.send("data_json/delivers.json")
    if page == "Track your shipment":
        find_parcel.find("data_json/delivers.json")




if __name__ == "__main__":
    main1()
