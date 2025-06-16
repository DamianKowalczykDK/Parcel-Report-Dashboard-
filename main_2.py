from typing import cast

import streamlit as st

from locker_streamlit import find_parcel
from locker_streamlit import send_parcel, report
from src.converter import (
    UserConverter, LockerConverter, ParcelConverter, DeliverConverter
)
from src.file_service import (
    UserReaderJson, LockerReaderJson, ParcelReaderJson, DeliverReaderJson, FileReader
)
from src.model import DeliversDataDict, UsersDataDict, LockersDataDict, ParcelsDataDict
from src.repository import (
    UserDataRepository, LockerDataRepository,
    ParcelDataRepository, DeliveryDataRepository, ParcelSummaryRepository,
)
from src.service import ParcelReportService
from src.validator import (
    UserDataDictValidator, LockerDataDictValidator,
    ParcelDataDictValidator, DeliversDataDictValidator
)


def main_2() -> None:


    user_repo = UserDataRepository(
        file_reader= cast(FileReader[UsersDataDict], UserReaderJson()),
        validator=UserDataDictValidator(),
        converter=UserConverter(),
        filename="data_json/users.json",
    )
    locker_repo = LockerDataRepository(
        file_reader=cast(FileReader[LockersDataDict], LockerReaderJson()),
        validator=LockerDataDictValidator(),
        converter=LockerConverter(),
        filename="data_json/lockers.json",
    )
    parcel_repo = ParcelDataRepository(
        file_reader=cast(FileReader[ParcelsDataDict], ParcelReaderJson()),
        validator=ParcelDataDictValidator(),
        converter=ParcelConverter(),
        filename="data_json/parcels.json",
    )
    delivery_repo = DeliveryDataRepository(
        file_reader=cast(FileReader[DeliversDataDict], DeliverReaderJson()),
        validator=DeliversDataDictValidator(),
        converter=DeliverConverter(),
        filename="data_json/delivers.json",
    )

    repository = ParcelSummaryRepository(user_repo, locker_repo, parcel_repo, delivery_repo)
    service = ParcelReportService(repository)
    st.title("Automated Parcel Delivery Monitor 📦")
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Select", ["Send Order", "Track your shipment", "Report"])

    match page:
        case "Send Order":
            send_parcel.send("data_json/delivers.json")
        case "Track your shipment":
            find_parcel.find("data_json/delivers.json")
        case "Report":
            st.subheader("Reports")
            if st.button("📊 Most Common Parcel Sizes per Locker"):
                report.report_most_common_parcel_sizes_per_locker(service=service)
            if st.button('📊 City Most Shipments by Size'):
                report.report_city_most_shipments_by_size(service=service)





if __name__ == "__main__":
    main_2()
