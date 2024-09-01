import os
from dotenv import load_dotenv, set_key
import secrets

# Генерация случайного ключа
SECRET_KEY = secrets.token_urlsafe(64)

# Путь к файлу .env в корне проекта
env_file_path = '.env'

# Создание .env файла, если он не существует
if not os.path.exists(env_file_path):
    with open(env_file_path, 'w') as f:
        f.write(f"SECRET_KEY={SECRET_KEY}\n")
else:
    # Если .env файл уже существует, обновите его ключ
    load_dotenv(env_file_path)
    set_key(env_file_path, "SECRET_KEY", SECRET_KEY)

print(f".env файл создан или обновлён с SECRET_KEY.")
