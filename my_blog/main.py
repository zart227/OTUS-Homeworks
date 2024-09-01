from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, posts, tags, index, contact
from config.settings import SECRET_KEY

app = FastAPI()

# SECRET_KEY = os.getenv("SECRET_KEY")

# Настройка сессий
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY) 

# Настройка статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")

# Подключение маршрутов
app.include_router(index.router, tags=["index"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(contact.router, prefix="/contact", tags=["contact"])
