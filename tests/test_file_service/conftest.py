from src.model import UsersDataDict
import pytest
import os
import json


@pytest.fixture
def users_data(user_1_data: UsersDataDict, user_2_data: UsersDataDict) -> list[UsersDataDict]:
    return [user_1_data, user_2_data]

@pytest.fixture
def users_file(tmpdir, users_data) -> str:
    file_path = os.path.join(tmpdir, "test_user.json")
    with open(file_path, "w") as file:
        json.dump(users_data, file)
    return file_path