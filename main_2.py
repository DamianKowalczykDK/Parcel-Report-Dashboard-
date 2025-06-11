from locker_streamlit import send_parcel
import streamlit as st

def main1() -> None:
    st.title("Automated Parcel Delivery Monitor 📦")
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Select", ["Send Order", "Track your shipment", "Report"])
    if page == "Send Order":
        send_parcel.send("data_json/delivers.json")

if __name__ == "__main__":
    main1()
