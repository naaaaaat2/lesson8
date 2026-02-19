import pytest
import requests
from . import config
from .helpers import random_project_name


@pytest.fixture
def create_project():
    url = f"{config.BASE_URL}/api-v2/projects"
    data = {
        "name": random_project_name(),
        "description": "Проект создан для тестов"
    }
    response = requests.post(url, json=data, headers=config.HEADERS)
    project = response.json()
    yield project
    # Удаляем созданный проект для чистоты, если API позволяет
    if "id" in project:
        requests.delete(
            f"{config.BASE_URL}/api-v2/projects/{project['id']}",
            headers=config.HEADERS
        )


# --- Тест создания проекта ---


def test_create_project_positive():
    url = f"{config.BASE_URL}/api-v2/projects"
    data = {
        "name": random_project_name(),
        "description": "Описание проекта"
    }
    response = requests.post(url, json=data, headers=config.HEADERS)
    assert response.status_code == 201, (
        f"Ожидался статус 201, "
        f"получен {response.status_code}"
    )
    resp_json = response.json()
    assert resp_json["name"] == data["name"]
    assert "id" in resp_json


def test_create_project_negative_missing_name():
    url = f"{config.BASE_URL}/api-v2/projects"
    data = {
        # Отсутствует name — обязательное поле
        "description": "Описание без имени"
    }
    response = requests.post(url, json=data, headers=config.HEADERS)
    assert response.status_code in (400, 422), (
        f"Ожидался 400 или 422, "
        f"получен {response.status_code}"
    )


# --- Тест обновления проекта ---


def test_update_project_positive(create_project):
    project = create_project
    url = f"{config.BASE_URL}/api-v2/projects/{project['id']}"
    update_data = {
        "name": random_project_name()
    }
    response = requests.put(url, json=update_data, headers=config.HEADERS)
    assert response.status_code == 200, (
        f"Ожидался статус 200, "
        f"получен {response.status_code}"
    )
    resp_json = response.json()
    assert resp_json["name"] == update_data["name"]


def test_update_project_negative_wrong_id():
    url = f"{config.BASE_URL}/api-v2/projects/0"  # Несуществующий id
    update_data = {
        "name": "Should Fail"
    }
    response = requests.put(url, json=update_data, headers=config.HEADERS)
    assert response.status_code == 404, (
        f"Ожидался 404, "
        f"получен {response.status_code}"
    )


# --- Тест получения проекта ---


def test_get_project_positive(create_project):
    project = create_project
    url = f"{config.BASE_URL}/api-v2/projects/{project['id']}"
    response = requests.get(url, headers=config.HEADERS)
    assert response.status_code == 200, (
        f"Ожидался 200, "
        f"получен {response.status_code}"
    )
    resp_json = response.json()
    assert resp_json["id"] == project["id"]


def test_get_project_negative_wrong_id():
    url = f"{config.BASE_URL}/api-v2/projects/9999999"
    response = requests.get(url, headers=config.HEADERS)
    assert response.status_code == 404, (
        f"Ожидался 404, "
        f"получен {response.status_code}"
    )
