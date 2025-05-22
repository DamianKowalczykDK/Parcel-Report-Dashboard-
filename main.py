from src.model import LockersDataDict, ParcelsDataDict, DeliversDataDict
from src.validator import LockerDataDictValidator, Validator, ParcelDataDictValidator, DeliversDataDictValidator


def main() -> None:
    # validator =  LockerDataDictValidator()
    #
    # lockers = {
    # "locker_id": "L002",
    # "city": "Los Angeles",
    # "latitude": 34.052235,
    # "longitude": -118.243683,
    # "compartments": {
    #   "small": 0,
    #   "medium": 0,
    #   "large": 0
    # }
    # }
    #
    # print(validator.validate(lockers))

    validator = ParcelDataDictValidator()
    parcel: ParcelsDataDict = {
    "parcel_id": "P67890",
    "height": 1,
    "length": 2,
    "weight": 3,
  }
    print(validator.validate(parcel))

  #   delivers: DeliversDataDict =  {
  #   "parcel_id": "P67890",
  #   "locker_id": "L002",
  #   "sender_email": "bob.jones@example.com",
  #   "receiver_email": "jane.smith@example.com",
  #   "sent_date": "2023-12-01",
  #   "expected_delivery_date": "2023-12-03"
  # }
  #
  #   validator = DeliversDataDictValidator()
  #   print(validator.validate(delivers))
    pass
if __name__ == '__main__':
    main()