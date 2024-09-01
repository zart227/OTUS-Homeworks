import os
from dotenv import load_dotenv

# Загрузите переменные окружения из .env файла
load_dotenv()

# Чтение настроек из переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = "access_token"