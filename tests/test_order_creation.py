"""Тесты создания заказа."""

import allure

from api.order_api import OrderApi


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, created_order):
        assert created_order.status_code == 200
        body = created_order.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, valid_ingredients):
        response = OrderApi.create_order(ingredients=valid_ingredients)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, created_order):
        assert created_order.status_code == 200
        body = created_order.json()
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