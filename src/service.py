from src.repository import ParcelSummaryRepository
from collections import defaultdict
from dataclasses import dataclass
from src.model import Parcel
from typing import Any
import logging

logging.basicConfig(level=logging.INFO)

NestedDefaultDict = defaultdict[str, defaultdict[str, int]]
SentCountsType = defaultdict[Any, defaultdict[str, int]]
ReceivedCountType = defaultdict[Any, defaultdict[str, int]]

@dataclass(eq=True, frozen=False)
class ParcelReportService:
    repository: ParcelSummaryRepository

    def most_common_parcel_sizes_per_locker(self) -> dict[str, list[str]]:
        result: NestedDefaultDict = defaultdict(lambda: defaultdict(int))
        parcels: dict[str, Parcel] = {p.parcel_id: p for p in self.repository.parcel_repo.get_data()}

        for deliver in self.repository.delivery_repo.get_data():
            parcel = parcels[deliver.parcel_id]

            size = Parcel.get_size(parcel.height, parcel.length)
            result[deliver.locker_id][size.value] += 1

        most_common = {}

        for locker_id, size_counts in result.items():
            if size_counts:
                max_count = max(size_counts.values())
                common_size = [size for size, count in size_counts.items() if count == max_count]
                most_common[locker_id] = common_size

        return most_common


    def city_most_shipments_by_size(self) -> dict[str, dict[str, str]]:
        users = {u.email: u for u in self.repository.user_repo.get_data()}
        parcels = {p.parcel_id: p for p in self.repository.parcel_repo.get_data()}
        delivers = self.repository.delivery_repo.get_data()

        sent_counts:  SentCountsType = defaultdict(lambda: defaultdict(int))
        received_counts:  ReceivedCountType = defaultdict(lambda: defaultdict(int))

        for deliver in delivers:
            parcel = parcels.get(deliver.parcel_id)
            sender = users.get(deliver.sender_email)
            receiver = users.get(deliver.receiver_email)
            if parcel and sender and receiver:
                size = Parcel.get_size(parcel.height, parcel.length)
                sent_counts[size.value][sender.city] += 1
                received_counts[size.value][receiver.city] += 1

        result: dict[Any, Any] = {
            "sent": {},
            "received": {},
        }

        for size, city in sent_counts.items():
            max_count = max(city.items(), key=lambda x: x[1])[0]
            result["sent"][size] = max_count

        for size, city in received_counts.items():
            max_count = max(city.items(), key=lambda x: x[1])[0]
            result["received"][size] = max_count

        return result
























