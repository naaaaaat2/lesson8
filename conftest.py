import pytest
import requests
from endpoints import AuthEndpoint, ProjectEndpoint


@pytest.fixture(scope="session")
def base_url():
    """Возвращает базовый URL API."""
    return "https://ru.yougile.com/api-v2"


@pytest.fixture(scope="session")
def auth_data():
    """
    Фикстура с данными для авторизации.
    Реальные данные для доступа к API Yougile.
    """
    return {
        "login": "nataliapavlyuk212@mail.ru",
        "password": "Younata1997",
        "companyId": "f6a8e686-b61a-4ebb-ad8b-2b4075d938c0"
    }


@pytest.fixture(scope="session")
def auth_token(base_url, auth_data):
    """
    Фикстура для получения токена авторизации.
    Выполняет POST запрос к /auth/keys и возвращает ключ.
    """
    auth_endpoint = AuthEndpoint(base_url)
    response = auth_endpoint.get_key(auth_data)
    
    print(f"\nСтатус ответа: {response.status_code}")
    print(f"Тело ответа: {response.text}")
    
    assert response.status_code == 201, f"Не удалось получить ключ API. Статус: {response.status_code}"
    
    token = auth_endpoint.response_json.get("key")
    assert token is not None, "В ответе отсутствует ключ"
    
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """Возвращает заголовки с авторизацией для последующих запросов."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def project_endpoint(base_url, auth_headers):
    """Фикстура для работы с проектами."""
    return ProjectEndpoint(base_url, auth_headers)


@pytest.fixture
def test_project_data():
    """Тестовые данные для создания проекта."""
    return {
        "title": "Тестовый проект для автотестов"
    }


@pytest.fixture
def created_project(project_endpoint, test_project_data):
    """
    Фикстура создает проект и возвращает его ID.
    """
    response = project_endpoint.create_project(test_project_data)
    assert response.status_code == 201
    project_id = project_endpoint.created_project_id
    yield project_id
    print(f"\nСоздан проект с ID: {project_id}")
