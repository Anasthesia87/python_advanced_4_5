from http import HTTPStatus

import pytest
import requests
from app.models.User import UserData


def test_service_availability(base_url):
    response = requests.get(f'{base_url}/status')
    assert response.json()['database']
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND)


@pytest.mark.usefixtures("clear_database")
def test_clear_database(base_url):
    response = requests.get(f"{base_url}/users")
    data = response.json()
    user_list = data if isinstance(data, list) else data.get('items', [])
    assert len(user_list) == 0, (
        f"База даных не пуста. Найдено пользователей: {len(user_list)}\n"
        f"Содержимое: {user_list}"
    )


@pytest.mark.usefixtures("fill_test_data")
def test_users(base_url):
    response = requests.get(f"{base_url}/api/users")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()['items']
    for user in user_list:
        UserData.model_validate(user)


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_list = users["items"]
    users_ids = [user["id"] for user in users_list]
    assert len(users_ids) == len(set(users_ids)), "Найдены дубликаты ID пользователей"


def test_user(base_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        UserData.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
