from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.models import User, get_db
from app.utils.security import verify_password, create_access_token, oauth2_scheme
from app.utils.cookies import set_message_cookie, get_message_from_cookie
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, COOKIE_NAME

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class RegisterForm(BaseModel):
    username: str
    password: str

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    message, message_type = get_message_from_cookie(request)
    return templates.TemplateResponse("login.html", {"request": request, "message": message, "message_type": message_type})

@router.post("/token", response_class=RedirectResponse)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        response = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
        # response.set_cookie(key="message", value="Incorrect username or password")
        # response.set_cookie(key="message_type", value="error")
        set_message_cookie(response,"Incorrect username or password","error")
        return response
    
    # Создание токена доступа
    access_token = create_access_token(data={"sub": user.username})
    
    # Настройка cookie для токена
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # время жизни cookie в секундах
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # время истечения срока действия
    )
    # response.set_cookie(key="message", value="Successfully logged in")
    # response.set_cookie(key="message_type", value="success")
    set_message_cookie(response,"Successfully logged in","success")
    return response

@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    message, message_type = get_message_from_cookie(request)
    return templates.TemplateResponse("registr.html", {"request": request, "message": message, "message_type": message_type})

@router.post("/register", response_class=RedirectResponse)
async def register(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.username == form_data.username).first()
    if existing_user:
        response = RedirectResponse(url="/auth/register", status_code=status.HTTP_302_FOUND)
        # response.set_cookie(key="message", value="Username already registered")
        # response.set_cookie(key="message_type", value="error")
        set_message_cookie(response,"Username already registered","error")
        return response
    
    new_user = User(username=form_data.username)
    new_user.set_password(form_data.password)
    db.add(new_user)
    db.commit()

    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    # response.set_cookie(key="message", value="User registered successfully")
    # response.set_cookie(key="message_type", value="success")
    set_message_cookie(response,"User registered successfully","success")
    return response

@router.get("/logout", response_class=RedirectResponse)
async def logout(response: Response):
    """
    Logout route that clears the user's cookie with the token.
    """
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    # Устанавливаем cookie с пустым значением и сроком истечения в прошлом, чтобы удалить его
    response.delete_cookie(COOKIE_NAME)
    # response.set_cookie(key="message", value="Successfully logged out")
    # response.set_cookie(key="message_type", value="success")
    set_message_cookie(response,"Successfully logged out","success")
    return response