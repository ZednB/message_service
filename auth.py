from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from users.models import User  # Замените на ваши модели и функции
from db import get_db

# Транспорт для аутентификации (например, через Cookie)
cookie_transport = CookieTransport(cookie_name="auth", cookie_secure=False)

# Бэкенд для аутентификации без хеширования
auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=lambda: None,  # Пропускаем использование хеширования
)

# Экземпляр FastAPIUsers
fastapi_users = FastAPIUsers[User, int](
    get_db,  # Замените на вашу функцию для получения базы данных пользователей
    [auth_backend],
)
