from src.repository import ParcelSummaryRepository
from src.model import Parcel, CompartmentsLarge
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


SendAndReceivedType = dict[str, defaultdict[CompartmentsLarge, dict[str, int]]]
NestedDefaultDict = defaultdict[str, defaultdict[str, int]]
ResultsDict = dict[str, dict[str, str | int]]

@dataclass(eq=True, frozen=False)
class ParcelReportService:
    """
    Service providing reports and statistics related to parcels, lockers, and deliveries.
    """

    repository: ParcelSummaryRepository

    def most_common_parcel_sizes_per_locker(self) -> dict[str, list[str]]:
        """
        Returns the most common parcel sizes per locker.

        Aggregates the parcel sizes for each locker and returns a dictionary
        where the key is the locker ID and the value is a list of the most common parcel size(s).
        """
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

    def city_most_shipments_by_size(self) -> dict[str, dict[str, str | int]]:
        """
        Returns cities with the most shipments by parcel size, split by sent and received.

        Returns a dictionary with keys 'sent' and 'received', each mapping parcel sizes to the city
        with the highest shipment count.
        """
        users = {u.email: u for u in self.repository.user_repo.get_data()}
        parcels = {p.parcel_id: p for p in self.repository.parcel_repo.get_data()}

        counts: SendAndReceivedType = {
            "sent": defaultdict(lambda: defaultdict(int)),
            "received": defaultdict(lambda: defaultdict(int)),
        }

        for deliver in self.repository.delivery_repo.get_data():
            parcel = parcels.get(deliver.parcel_id)
            sender = users.get(deliver.sender_email)
            receiver = users.get(deliver.receiver_email)
            if parcel and sender and receiver:
                size = Parcel.get_size(parcel.height, parcel.length)
                counts["sent"][size][sender.city] += 1
                counts["received"][size][receiver.city] += 1

        result: ResultsDict = {
            "sent": {},
            "received": {},
        }

        for sent_received in ["sent", "received"]:
            for size, cities in counts[sent_received].items():
                most_common_cities = max(cities.items(), key=lambda x: x[1])[0]
                result[sent_received][size.value] = most_common_cities

        return result

    def max_days_between_sent_and_expected(self) -> dict[str, int]:
        """
        Calculates the maximum number of days between the sent date and expected delivery date per sender.

        Returns a dictionary mapping sender email addresses to the maximum delivery duration (in days).
        """
        result: defaultdict[str, int] = defaultdict(int)

        for deliver in self.repository.delivery_repo.get_data():
            sent_date = datetime.strptime(deliver.sent_date ,"%Y-%m-%d")
            expected_date = datetime.strptime(deliver.expected_delivery_date ,"%Y-%m-%d")
            days = (expected_date - sent_date).days
            result[deliver.sender_email] = max(result[deliver.sender_email], days)

        max_delivery = max(result.values(), default=0)
        counts = {sender: days for sender, days in result.items() if max_delivery == days}
        return counts

    def is_parcel_limit_in_locker_exceeded(self) -> dict[str, dict[CompartmentsLarge, int]]:
        """
        Checks if any parcel locker compartment has exceeded its parcel limit.

        Returns a dictionary mapping locker IDs to dictionaries of compartment sizes and their remaining capacity.
        Logs a warning if any compartment capacity goes below zero.
        """
        result: defaultdict[str, dict[CompartmentsLarge, int]] = defaultdict(dict)
        parcels = {p.parcel_id: p for p in self.repository.parcel_repo.get_data()}

        for locker in self.repository.locker_repo.get_data():
            result[locker.locker_id] = dict(locker.compartments)

        for deliver in self.repository.delivery_repo.get_data():
            parcel = parcels[deliver.parcel_id]
            size = Parcel.get_size(parcel.height, parcel.length)
            result[deliver.locker_id][size] -= 1
            if result[deliver.locker_id][size] < 0:
                logging.warning(f'No places available {deliver.locker_id} for {size}')

        return result

