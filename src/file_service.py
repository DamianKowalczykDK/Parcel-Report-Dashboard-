from src.model import User, Parcel, Locker, Deliver
import json

class FileReader[T]:
    @staticmethod
    def read(file_name: str) -> list[T]:
        with open(file_name, 'r', encoding="utf-8") as file:
            return json.load(file)

class UserReaderJson(FileReader[User]):
    pass

class LockerReaderJson(FileReader[Locker]):
    pass

class ParcelReaderJson(FileReader[Parcel]):
    pass

class DeliverReaderJson(FileReader[Deliver]):
    pass

class FileWriter[T]:
    @staticmethod
    def write(file_name: str, data: list[T]) -> None:
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file)

class UserWriterJson(FileWriter[User]):
    pass

class LockerWriterJson(FileWriter[Locker]):
    pass

class ParcelWriterJson(FileWriter[Parcel]):
    pass

class DeliverWriterJson(FileWriter[Deliver]):
    pass