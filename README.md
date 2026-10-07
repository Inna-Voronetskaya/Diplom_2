# Diploma_2 — API-тесты Stellar Burgers

Автотесты для API сервиса Stellar Burgers.

## Что тестируется

- **Создание пользователя** (`POST /api/auth/register`)
- **Авторизация** (`POST /api/auth/login`)
- **Создание заказа** (`POST /api/orders`)

## Структура проекта

- `api/` — API-клиенты (`user_api.py`, `order_api.py`)
- `helpers/` — генератор тестовых данных
- `tests/` — тесты
- `config.py` — конфигурация (BASE_URL)
- `conftest.py` — фикстуры

## Установка

```bash
pip install -r requirements.txt