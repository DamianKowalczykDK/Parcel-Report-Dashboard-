from src.model import User, Parcel, Locker, Deliver
import json

class FileReader[T]:
    """
    Generic file reader class for reading JSON data_json into a list of type T.
    """
    @staticmethod
    def read(file_name: str) -> list[T]:
        """
        Reads JSON data_json from a file and returns it as a list of objects of type T.

        Args:
            file_name (str): Path to the JSON file.

        Returns:
            list[T]: List of deserialized objects.
        """
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)

class UserReaderJson(FileReader[User]):
    """
    File reader specialized for User objects.
    """
    pass

class LockerReaderJson(FileReader[Locker]):
    """
    File reader specialized for Locker objects.
    """
    pass

class ParcelReaderJson(FileReader[Parcel]):
    """
    File reader specialized for Parcel objects.
    """
    pass

class DeliverReaderJson(FileReader[Deliver]):
    """
    File reader specialized for Deliver objects.
    """
    pass

class FileWriter[T]:
    """
    Generic file writer class for writing a list of objects of type T to a JSON file.
    """
    @staticmethod
    def write(file_name: str, data: list[T]) -> None:
        """
        Writes a list of objects to a JSON file.

        Args:
            file_name (str): Path to the JSON file.
            data (list[T]): List of objects to serialize.
        """
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

class UserWriterJson(FileWriter[User]):
    """
    File writer specialized for User objects.
    """
    pass

class LockerWriterJson(FileWriter[Locker]):
    """
    File writer specialized for Locker objects.
    """
    pass

class ParcelWriterJson(FileWriter[Parcel]):
    """
    File writer specialized for Parcel objects.
    """
    pass

class DeliverWriterJson(FileWriter[Deliver]):
    """
    File writer specialized for Deliver objects.
    """
    pass