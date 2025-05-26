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


def main():
    # Tworzenie repozytoriów - ścieżki do plików JSON
    user_repo = UserDataRepository(
        file_reader=UserReaderJson(),
        validator=UserDataDictValidator(),
        converter=UserConverter(),
        filename="data/users.json",
    )
    locker_repo = LockerDataRepository(
        file_reader=LockerReaderJson(),
        validator=LockerDataDictValidator(),
        converter=LockerConverter(),
        filename="data/lockers.json",
    )
    parcel_repo = ParcelDataRepository(
        file_reader=ParcelReaderJson(),
        validator=ParcelDataDictValidator(),
        converter=ParcelConverter(),
        filename="data/parcels.json",
    )
    delivery_repo = DeliveryDataRepository(
        file_reader=DeliverReaderJson(),
        validator=DeliversDataDictValidator(),
        converter=DeliverConverter(),
        filename="data/delivers.json",
    )

    repository = ParcelSummaryRepository(user_repo, locker_repo, parcel_repo, delivery_repo)
    service = ParcelReportService(repository)
    service.most_common_parcel_sizes_per_locker()
    service.city_most_shipments_by_size()




if __name__ == "__main__":
    main()