"""Тесты создания пользователя."""

import allure
import pytest

from api.user_api import UserApi


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, unique_user_data, user_cleanup):
        response = UserApi.register(
            email=unique_user_data["email"],
            password=unique_user_data["password"],
            name=unique_user_data["name"],
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == unique_user_data["email"]
        assert body["user"]["name"] == unique_user_data["name"]
        assert "accessToken" in body
        assert "refreshToken" in body

        user_cleanup(body["accessToken"])

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_already_registered_user(self, unique_user_data, user_cleanup):
        # Создаём пользователя ВНУТРИ теста (не через registered_user)
        first_response = UserApi.register(
            email=unique_user_data["email"],
            password=unique_user_data["password"],
            name=unique_user_data["name"],
        )
        assert first_response.status_code == 200
        user_cleanup(first_response.json()["accessToken"])

        # Повторная регистрация
        response = UserApi.register(
            email=unique_user_data["email"],
            password=unique_user_data["password"],
            name=unique_user_data["name"],
        )

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, unique_user_data, missing_field):
        data = unique_user_data.copy()
        data.pop(missing_field)

        response = UserApi.register(
            email=data.get("email", ""),
            password=data.get("password", ""),
            name=data.get("name", ""),
        )

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"