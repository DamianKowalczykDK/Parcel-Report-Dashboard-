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
from typing import cast


def main():
    user_repo = UserDataRepository(
        file_reader=cast(FileReader[UsersDataDict], UserReaderJson()),
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
    service.city_most_shipments_by_size()
    service.is_parcel_limit_in_locker_exceeded()
    print(service.max_days_between_sent_and_expected())

if __name__ == "__main__":
    main()