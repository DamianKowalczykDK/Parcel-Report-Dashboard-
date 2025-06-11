from src.model import UsersDataDict, LockersDataDict, ParcelsDataDict, DeliversDataDict
from email_validator import validate_email, EmailNotValidError
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import override, cast
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


class Validator[T](ABC):
    """
    Abstract base class for data_json validation.

    Subclasses must implement the `validate` method for their specific data_json type.
    """
    @abstractmethod
    def validate(self, data: T) -> bool: #pragma: no cover

        pass

    @staticmethod
    def has_required_keys(data: T, keys: list[str]) -> bool:
        """
    Checks whether all required keys are present in the given data_json.

    Args:
        data (T): The data_json to validate, typically a dictionary or object.
        keys (list[str]): A list of required key names.

    Returns:
        bool: True if all keys are present, False otherwise.
    """
        missing_keys = []
        for key in keys:
            if isinstance(data, dict):
                if key not in data:
                    missing_keys.append(key)
            elif not hasattr(data, key):
                missing_keys.append(key)
        if missing_keys:
            logging.error(f"Missing required keys: {missing_keys}")
            return False
        return True

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
                Validates the format of an email address using the `email_validator` library.

                Args:
                    email: The email address to validate.

                Returns:
                    True if the email is valid; otherwise, False.
                """
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            logging.error(str(e))
            return False

    @staticmethod
    def is_positive(data: int | str) -> bool:
        """
                Checks if a given value is a positive number. Supports both int and numeric string.

                Args:
                    data: The input value to check.

                Returns:
                    True if the value is a positive number; otherwise, False.
                """
        match data:
            case int(value) if value > 0:
                return True
            case str(value):
                try:
                    str_value = int(value)
                    return str_value > 0
                except ValueError as e:
                    logging.error(str(e))
                    return False
            case _:
                return False

@dataclass
class UserDataDictValidator(Validator[UsersDataDict]):
    """
        Validator for user data_json (UserDataDict).
        """
    required_keys: list[str] = field(default_factory=lambda:["email", "name", "surname", "city", "latitude", "longitude"])

    @override
    def validate(self, data: UsersDataDict) -> bool:
        """
                Validates user data_json by checking required fields and email format.
                """
        if len(self.required_keys) == 0 or not self.has_required_keys(data, self.required_keys):
            return False
        return Validator.is_valid_email(data['email'])

@dataclass
class LockerDataDictValidator(Validator[LockersDataDict]):
    """
       Validator for locker data_json (LockersDataDict).
       """
    required_keys: list[str] = field(default_factory=lambda:["locker_id", "city", "latitude", "longitude", "compartments"])

    @override
    def validate(self, data: LockersDataDict) -> bool:
        """
                Validates locker data_json by checking structure, required fields, and if compartment values are positive integers.
                """
        if len(self.required_keys) == 0 or not self.has_required_keys(data, self.required_keys):
            return False
        if not isinstance(data["compartments"], dict):
            logging.error("Field 'compartments' is not a dictionary")
            return False
        for compartment, count in data["compartments"].items():
            if not self.is_positive(count):
                logging.error(f"Compartment {compartment} is not positive")
                return False
        return True


@dataclass
class ParcelDataDictValidator(Validator[ParcelsDataDict]):
    """
        Validator for parcel data_json (ParcelsDataDict).
        """
    required_keys: list[str] = field(default_factory=lambda:["parcel_id", "height", "length", "weight"])

    @override
    def validate(self, data: ParcelsDataDict) -> bool:
        """
                Validates parcel data_json by checking required fields and ensuring height, length, and weight are positive.
                """
        if len(self.required_keys) == 0 or not self.has_required_keys(data, self.required_keys):
            return False

        for key in ("height", "length", "weight"):
            if not self.is_positive(cast(dict, data)[key]):
                return False

        return True

@dataclass
class DeliversDataDictValidator(Validator[DeliversDataDict]):
    """
        Validator for delivery data_json (DeliversDataDict).
        """

    required_keys: list[str] = field(default_factory=lambda: [
        "parcel_id", "locker_id", "sender_email", "receiver_email", "sent_date", "expected_delivery_date"]
    )
    @override
    def validate(self, data: DeliversDataDict) -> bool:
        """
                Validates delivery data_json by checking required fields, ensuring sender and receiver are different,
                and that the delivery dates are chronologically correct.
                """

        if len(self.required_keys) == 0 or not self.has_required_keys(data, self.required_keys):
            return False

        if not self.is_valid_email(data["sender_email"]):
            logging.warning("Sender email is not valid")
            return False
        if not self.is_valid_email(data["receiver_email"]):
            logging.warning("Receiver email is not valid")
            return False

        if data['sender_email'] == data['receiver_email']:
            logging.warning('Email cannot be the same as sender address')
            return False

        sent_date = datetime.strptime(data['sent_date'], "%Y-%m-%d")
        expected_delivery_date = datetime.strptime(data['expected_delivery_date'], "%Y-%m-%d")

        if sent_date >= expected_delivery_date:
            logging.warning('Delivery date cannot be earlier than expected delivery date')
            return False

        return True
