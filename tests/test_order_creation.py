"""Тесты создания заказа."""

import allure
import pytest

from api.order_api import OrderApi


@pytest.fixture(scope="module")
def valid_ingredients():
    """Получаем валидные ID ингредиентов с сервера (один раз на модуль)."""
    response = OrderApi.get_ingredients()
    assert response.status_code == 200
    ingredients = response.json()["data"]
    return [ingredients[0]["_id"], ingredients[1]["_id"]]


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, access_token, valid_ingredients):
        response = OrderApi.create_order(
            ingredients=valid_ingredients, access_token=access_token
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, valid_ingredients):
        # API позволяет создавать гостевые заказы без авторизации
        response = OrderApi.create_order(ingredients=valid_ingredients)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, access_token, valid_ingredients):
        response = OrderApi.create_order(
            ingredients=valid_ingredients, access_token=access_token
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, access_token):
        response = OrderApi.create_order(
            ingredients=[], access_token=access_token
        )

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash(self, access_token):
        response = OrderApi.create_order(
            ingredients=["invalid_hash_123"], access_token=access_token
        )

        assert response.status_code == 500