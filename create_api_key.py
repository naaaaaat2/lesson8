import requests


# Введите ваш API URL ниже, например: https://api-v2/auth/keys
BASE_URL = "https://api-v2/auth/keys"


# Введите ваши учетные данные
login = "some@example.com"
password = "topsecret"


# Введите ID компании
companyId = "9347006b-dc75-4550-97d5-3008ba00d4a0"


# Заголовки
headers = {
    'Content-Type': 'application/json'
}


# Тело запроса
payload = {
    "login": login,
    "password": password,
    "companyId": companyId
}


# Отправка запроса
response = requests.post(
    f"{BASE_URL}/api-v2/auth/keys",
    headers=headers,
    json=payload
)


# Обработка ответа
if response.status_code == 201:
    data = response.json()
    api_key = data.get('key')
    if api_key:
        print(f"Получен ключ: {api_key}")
    else:
        print("Ключа в ответе не найдено.")
else:
    print(f"Ошибка: Status {response.status_code}")
    print(f"Текст ответа: {response.text}")
