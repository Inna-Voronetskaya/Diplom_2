"""Тесты авторизации пользователя."""

import allure
import pytest

from api.user_api import UserApi


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, registered_user, unique_user_data):
        response = UserApi.login(
            email=unique_user_data["email"],
            password=unique_user_data["password"],
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == unique_user_data["email"]
        assert body["user"]["name"] == unique_user_data["name"]
        assert "accessToken" in body
        assert "refreshToken" in body

    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize(
        "email, password",
        [
            ("wrong_email@yandex.ru", "password123"),
            ("test@yandex.ru", "wrong_password"),
            ("wrong@yandex.ru", "wrong_password"),
        ],
    )
    def test_login_with_wrong_credentials(self, email, password):
        response = UserApi.login(email=email, password=password)

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"