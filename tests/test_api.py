import requests
from tests.conftest import base_url


def test_api_create_user(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()
    values_equal = (all
                    (new_user[key] == body[key]
                     for key in new_user
                     if key in body))
    assert values_equal

    delete_response = requests.delete(f"{base_url}/api/users/{new_user['id']}")
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_api_get_user_after_create_user(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()
    response = requests.get(f"{base_url}/api/users/{new_user['id']}")

    user_from_api = response.json()
    values_equal = all(
        new_user[key] == user_from_api[key]
        for key in new_user
        if key in user_from_api)
    assert values_equal

    delete_response = requests.delete(f"{base_url}/api/users/{new_user['id']}")
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_api_get_list_users_after_create_user(base_url, fill_test_data, clear_database):
    response = requests.get(f"{base_url}/api/users")
    assert response.status_code == 200, f"Не удалось получить список пользователей: {response.text}"
    initial_users = response.json()

    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    response = requests.get(f"{base_url}/api/users")
    users_list_from_api = response.json()
    users = users_list_from_api["items"]
    new_user_found = any(user['id'] == new_user['id'] for user in users)

    assert new_user_found, "Новый пользователь не найден в списке"

    values_equal = all(
        fill_test_data[key] == users_list_from_api[key] for key in fill_test_data if key in users_list_from_api)
    assert values_equal
    assert len(users_list_from_api["items"]) == len(initial_users["items"]) + 1

def test_api_update_patch_user_all_data(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    update_body = {
        "email": "new_valid@example.com",
        "first_name": "new_test_first_name",
        "last_name": "new_test_last_name",
        "avatar": "https://newexample.com/avatar.jpg"
    }

    update_response = requests.patch(f"{base_url}/api/users/{new_user['id']}", json=update_body)
    assert update_response.status_code == 200, f"Не удалось обновить пользователя: {update_response.text}"

    get_response = requests.get(f"{base_url}/api/users/{new_user['id']}")
    updated_user = get_response.json()

    for field, value in update_body.items():
        assert updated_user[field] == value, f"Поле {field} не обновилось"

    delete_response = requests.delete(f"{base_url}/api/users/{new_user['id']}")
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"


def test_delete_user_after_create(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()

    delete_response = requests.delete(f"{base_url}/api/users/{new_user['id']}")
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"

    response_get_after_delete = requests.get(f"{base_url}/users/{id}")
    assert response_get_after_delete.status_code == 404

    response_delete_after_delete = requests.delete(f"{base_url}/users/{id}")
    assert response_delete_after_delete.status_code == 404


def test_api_create_user_with_invalid_method(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.put(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 405, f"Ожидается ошибка 405, но получен статус: {create_response.status_code}"


def test_api_create_user_with_invalid_data(base_url):
    body = {
        "email": "invalid_email",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 500, f"Ожидается ошибка 500, но получен статус: {create_response.status_code}"


def test_api_create_user_without_email(base_url):
    body = {
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 500, f"Ожидается ошибка 500, но получен статус: {create_response.status_code}"
