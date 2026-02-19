import os

BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://yougile.ru")
TOKEN = os.getenv("YOUGILE_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
