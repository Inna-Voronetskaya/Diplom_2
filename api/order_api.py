"""API-клиент для работы с заказами и ингредиентами."""

import allure
import requests

from config import BASE_URL


class OrderApi:
    """Методы для работы с эндпоинтами заказов и ингредиентов."""

    @staticmethod
    @allure.step("Получение списка ингредиентов: GET /ingredients")
    def get_ingredients():
        """Получение списка всех ингредиентов."""
        return requests.get(f"{BASE_URL}/api/ingredients")

    @staticmethod
    @allure.step("Создание заказа: POST /orders")
    def create_order(ingredients, access_token=None):
        """Создание заказа с опциональной авторизацией."""
        headers = {}
        if access_token:
            headers["Authorization"] = access_token
        return requests.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": ingredients},
            headers=headers,
        )