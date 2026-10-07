"""Генерация тестовых данных."""

import uuid


def generate_unique_user():
    """Генерирует уникальные данные пользователя."""
    uid = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{uid}@yandex.ru",
        "password": "password123",
        "name": f"User_{uid}",
    }