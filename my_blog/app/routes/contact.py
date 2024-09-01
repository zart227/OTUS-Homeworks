from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/contact", name="contact")
async def get_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})
