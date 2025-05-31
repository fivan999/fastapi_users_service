# Cервис для работы с пользователями на FastAPI
## Установка и запуск
### Склонировать репозиторий
```
git clone https://github.com/fivan999/fastapi_users_service
```
### Конфигурация
Создайте .env файл в корне проекта (пример .env файла - .env.example) <br>
В нем нужно указать значения:<br>
- JWT_SECRET_KEY (секретный ключ для генерации jwt токена)<br>
- POSTGRES_DB (имя базы данных)
- POSTGRES_HOST (хост базы данных)
- POSTGRES_USER (имя пользователя базы данных)
- POSTGRES_PASSWORD (пароль базы данных, по умолчанию - password)
- POSTGRES_PORT (порт базы данных)
- ACCESS_TOKEN_EXPIRE_SECONDS (время валидности access токена в секундах)
- REFRESH_TOKEN_EXPIRE_SECONDS (время валидности refresh токена в секундах)
### Для разработки
1. Установить [Python 3.12](https://www.python.org/downloads/)
2. Установить [uv](https://docs.astral.sh/uv/)
3. Установить зависимости через uv
   ```bash
   uv sync
   ```
4. Установить [pre-commit](https://pre-commit.com/) хуки:

   ```bash
   uv tool install pre-commit --with pre-commit-uv
   ```
### Запустить проект
```bash
docker compose up
```
### Запуск тестов
```bash
docker compose -f docker-compose-test.yml up -d --build
docker exec fastapi_app /bin/sh -c "pytest tests/ && exit"
```