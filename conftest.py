"""Фикстуры для тестов."""

import pytest

from api.user_api import UserApi
from api.order_api import OrderApi  # <-- Добавлен импорт
from helpers.data_generator import generate_unique_user


@pytest.fixture
def unique_user_data():
    """Генерирует уникальные данные для регистрации (без запроса к API)."""
    return generate_unique_user()


@pytest.fixture
def user_cleanup():
    """
    Фикстура для очистки созданных пользователей.
    Возвращает функцию, в которую нужно передать accessToken.
    """
    tokens_to_delete = []

    def _add_token(access_token):
        tokens_to_delete.append(access_token)

    yield _add_token

    for token in tokens_to_delete:
        if token:
            try:
                UserApi.delete(token)
            except Exception:
                pass


@pytest.fixture
def registered_user(unique_user_data, user_cleanup):
    """Создаёт пользователя для тестов авторизации и заказов."""
    response = UserApi.register(
        email=unique_user_data["email"],
        password=unique_user_data["password"],
        name=unique_user_data["name"],
    )

    if response.status_code == 200:
        user_cleanup(response.json()["accessToken"])

    yield response


@pytest.fixture
def access_token(registered_user):
    """Возвращает accessToken зарегистрированного пользователя."""
    return registered_user.json()["accessToken"]


# --- ПЕРЕНЕСЕННАЯ ФИКСТУРА ---
@pytest.fixture(scope="session")
def valid_ingredients():
    """Получаем валидные ID ингредиентов с сервера (один раз на сессию)."""
    response = OrderApi.get_ingredients()
    assert response.status_code == 200
    ingredients = response.json()["data"]
    return [ingredients[0]["_id"], ingredients[1]["_id"]]