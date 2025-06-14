from src.file_service import (
    UserReaderJson, LockerReaderJson, ParcelReaderJson, DeliverReaderJson
)
from src.service  import ParcelReportService
from src.validator import (
    UserDataDictValidator, LockerDataDictValidator,
    ParcelDataDictValidator, DeliversDataDictValidator
)
from src.converter import (
    UserConverter, LockerConverter, ParcelConverter, DeliverConverter
)
from src.repository import (
    UserDataRepository, LockerDataRepository,
    ParcelDataRepository, DeliveryDataRepository, ParcelSummaryRepository,
)

from locker_streamlit import find_parcel
def main():

    # Tworzenie repozytoriów - ścieżki do plików JSON
    user_repo = UserDataRepository(
        file_reader=UserReaderJson(),
        validator=UserDataDictValidator(),
        converter=UserConverter(),
        filename="data_json/users.json",
    )
    locker_repo = LockerDataRepository(
        file_reader=LockerReaderJson(),
        validator=LockerDataDictValidator(),
        converter=LockerConverter(),
        filename="data_json/lockers.json",
    )
    parcel_repo = ParcelDataRepository(
        file_reader=ParcelReaderJson(),
        validator=ParcelDataDictValidator(),
        converter=ParcelConverter(),
        filename="data_json/parcels.json",
    )
    delivery_repo = DeliveryDataRepository(
        file_reader=DeliverReaderJson(),
        validator=DeliversDataDictValidator(),
        converter=DeliverConverter(),
        filename="data_json/delivers.json",
    )

    repository = ParcelSummaryRepository(user_repo, locker_repo, parcel_repo, delivery_repo)
    service = ParcelReportService(repository)
    # service.city_most_shipments_by_size()
    # service.is_parcel_limit_in_locker_exceeded()
    service.max_days_between_sent_and_expected()




if __name__ == "__main__":
    main()