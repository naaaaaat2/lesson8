import random
import string


def random_project_name(length=10):
    """Генерирует случайное имя проекта из латинских букв."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))
