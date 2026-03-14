import requests
from requests import Response


class BaseEndpoint:
    """Базовый класс для всех эндпоинтов."""
    
    response: Response
    response_json: dict
    
    def check_status_code_is(self, expected_code: int):
        """Проверка кода ответа."""
        assert self.response.status_code == expected_code, \
            f"Ожидался код {expected_code}, получен {self.response.status_code}"
    
    def check_status_code_is_200(self):
        self.check_status_code_is(200)
    
    def check_status_code_is_201(self):
        self.check_status_code_is(201)
    
    def check_status_code_is_400(self):
        self.check_status_code_is(400)
    
    def check_status_code_is_401(self):
        self.check_status_code_is(401)
    
    def check_status_code_is_403(self):
        self.check_status_code_is(403)
    
    def check_status_code_is_404(self):
        self.check_status_code_is(404)


class AuthEndpoint(BaseEndpoint):
    """Класс для работы с авторизацией."""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.url = f"{self.base_url}/auth/keys"
    
    def get_key(self, auth_data: dict) -> Response:
        """
        Получение ключа авторизации.
        
        Args:
            auth_data: Словарь с полями login, password, companyId
        """
        self.response = requests.post(
            self.url,
            json=auth_data
        )
        
        if self.response.status_code == 201:
            self.response_json = self.response.json()
        
        return self.response


class ProjectEndpoint(BaseEndpoint):
    """Класс для работы с проектами."""
    
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.projects_url = f"{self.base_url}/projects"
        self.created_project_id = None
    
    def create_project(self, body: dict) -> Response:
        """
        POST /api-v2/projects - создание проекта.
        
        Args:
            body: Словарь с данными проекта (title обязателен, users опционально)
        """
        self.response = requests.post(
            self.projects_url,
            json=body,
            headers=self.headers
        )
        
        if self.response.status_code == 201:
            self.response_json = self.response.json()
            self.created_project_id = self.response_json.get("id")
        
        return self.response
    
    def get_project(self, project_id: str) -> Response:
        """
        GET /api-v2/projects/{id} - получение проекта по ID.
        
        Args:
            project_id: ID проекта
        """
        self.response = requests.get(
            f"{self.projects_url}/{project_id}",
            headers=self.headers
        )
        
        if self.response.status_code == 200:
            self.response_json = self.response.json()
        
        return self.response
    
    def update_project(self, project_id: str, body: dict) -> Response:
        """
        PUT /api-v2/projects/{id} - обновление проекта.
        
        Args:
            project_id: ID проекта
            body: Словарь с обновленными данными (title и/или users)
        """
        self.response = requests.put(
            f"{self.projects_url}/{project_id}",
            json=body,
            headers=self.headers
        )
        
        if self.response.status_code == 200:
            self.response_json = self.response.json()
        
        return self.response
