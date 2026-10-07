"""API-клиент для работы с пользователями."""

import allure
import requests

from config import BASE_URL


class UserApi:
    """Методы для работы с эндпоинтами авторизации и регистрации."""

    @staticmethod
    @allure.step("Регистрация пользователя: POST /auth/register")
    def register(email, password, name):
        """Регистрация нового пользователя."""
        return requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": email, "password": password, "name": name},
        )

    @staticmethod
    @allure.step("Авторизация пользователя: POST /auth/login")
    def login(email, password):
        """Авторизация пользователя."""
        return requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email, "password": password},
        )

    @staticmethod
    @allure.step("Удаление пользователя: DELETE /auth/user")
    def delete(access_token):
        """Удаление пользователя (для очистки после теста)."""
        return requests.delete(
            f"{BASE_URL}/api/auth/user",
            headers={"Authorization": access_token},
        )