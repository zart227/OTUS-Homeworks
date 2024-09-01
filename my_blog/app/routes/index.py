from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import get_db
from app.utils.security import get_current_user_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request, db: Session = Depends(get_db)):
        print('Index route')  # Отладочное сообщение
        url_path=request.url.path
        print(f"URL path: {url_path}")
        cookie=request.cookies.get('access_token')
        print(f'access_token: {cookie}')
        try:
                current_user=get_current_user_from_cookie(request, db)        
        except:
                current_user = None
        context = {
                "current_user": current_user,
                "request": request,
        }        
        return templates.TemplateResponse("index.html", context)
