from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import get_db
from app.utils.security import get_current_user_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/contact", name="contact")
async def get_contact(request: Request, db: Session = Depends(get_db)):
    try:
        current_user=get_current_user_from_cookie(request, db)        
    except:
        current_user = None
    context = {
        "current_user": current_user,
        "request": request,
    }
    return templates.TemplateResponse("contact.html", context)
