from src.service import ParcelReportService
from src.model import CompartmentsLarge
from dataclasses import dataclass
from pandas import DataFrame
import pandas as pd

@dataclass
class ReportService:
    service: ParcelReportService

    def report_most_common_parcel_sizes_per_locker(self) -> DataFrame:
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
        data = self.service.most_common_parcel_sizes_per_locker()

        df = pd.DataFrame([
            {"Locker ID": locker_id, "Most Common Size(s)": ", ".join(sizes)} for locker_id, sizes in data.items()])

        return df

    def report_city_most_shipments_by_size(self) -> DataFrame:
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
        data = self.service.city_most_shipments_by_size()

        df = pd.DataFrame([
            {
                "sent/received": sent_received,
                "small": size_city.get("small"),
                "medium": size_city.get("medium"),
                "large": size_city.get("large"),

            }
            for sent_received, size_city in data.items()])


        return df

    def report_max_days_between_sent_and_expected(self) -> DataFrame:
        """
        Generates and displays a Streamlit table showing the maximum number of days
        between when a parcel was sent and the expected delivery date for each email.

        Retrieves data from the given ParcelReportService, converts it into a pandas DataFrame,
        and renders it as an interactive table in Streamlit.

        Args:
            service (ParcelReportService): The service object providing parcel report data.

        Returns:
            None
        """
        data = self.service.max_days_between_sent_and_expected()

        df = pd.DataFrame([
            {
                "email": email,
                "day": day
            }
            for email, day in data.items()])

        return df

    def report_is_parcel_limit_in_locker_exceeded(self) -> DataFrame:
        """
        Displays a Streamlit dataframe indicating whether the parcel limit in each locker
        has been exceeded, broken down by compartment size (Small, Medium, Large).

        Fetches the data from the provided ParcelReportService, formats it into a pandas DataFrame,
        and shows the counts of parcels per size category for each locker.

        Args:
            service (ParcelReportService): The service providing parcel limit data per locker.

        Returns:
            None
        """
        data = self.service.is_parcel_limit_in_locker_exceeded()


        df = pd.DataFrame([
            {
                "Locker ID": locker_id,
                "Small": size.get(CompartmentsLarge.SMALL, 0),
                "Medium": size.get(CompartmentsLarge.MEDIUM, 0),
                "Large": size.get(CompartmentsLarge.LARGE, 0),
            }
            for locker_id, size in data.items()
        ])

        return df

