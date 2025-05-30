from src.model import Parcel, Locker, Deliver
from src.repository import ParcelSummaryRepository
import pytest
import logging


def test_initial_state_empty_cache(
        parcel_summary_repo: ParcelSummaryRepository
) -> None:

    assert parcel_summary_repo._parcel_summary == {}

def test_build_parcel_summary(
        parcel_summary_repo: ParcelSummaryRepository,
        parcel_1: Parcel,
        locker_1: Locker,
          ) -> None:

    summary = parcel_summary_repo.parcel()
    locker1 = locker_1.locker_id
    deliver = summary[locker1][parcel_1.parcel_id]

    assert parcel_1.parcel_id in summary[locker_1.locker_id]
    assert deliver == 0


def test_invalid_entry_logs_warning(
        parcel_summary_repo: ParcelSummaryRepository,
        caplog: pytest.LogCaptureFixture) -> None:

    invalid_deliver = Deliver(
        parcel_id="P12345",
        locker_id="L0015687",
        sender_email="john.doe@example.com",
        receiver_email="jane.smith@example.com",
        sent_date="2023-12-01",
        expected_delivery_date="2023-12-05"
    )

    delivers = parcel_summary_repo.delivery_repo.get_data()
    delivers.append(invalid_deliver)

    with caplog.at_level(logging.WARNING):
        _ = parcel_summary_repo.parcel()
    assert any("not available" in record.message  for record in caplog.records)
