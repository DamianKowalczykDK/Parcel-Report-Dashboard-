from src.file_service import UserReaderJson, UserWriterJson
from src.model import User, UsersDataDict
import os.path


def test_user_read_file_service(users_file: str, users_data: list[UsersDataDict]) -> None:
    reader = UserReaderJson()
    users = reader.read(users_file)
    assert users == users_data


def test_user_write_file_service(users_data: list[User], users_file: str) -> None:
    file_path = os.path.join('test_user.json', users_file)
    writer = UserWriterJson()
    writer.write(file_path, users_data)
    assert users_file == file_path

