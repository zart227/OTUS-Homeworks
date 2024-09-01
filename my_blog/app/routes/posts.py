from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.models import Post, Tag, User, get_db
from app.utils.security import get_current_user
from app.utils.cookies import set_message_cookie, get_message_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class PostCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class PostUpdate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

@router.get("/", response_class=HTMLResponse, name="get_posts")
async def get_posts(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    message, message_type = get_message_from_cookie(request)
    context = {
        "current_user": current_user,
        "request": request,
        "posts": posts, 
        "message": message, 
        "message_type": message_type
    }
    return templates.TemplateResponse("posts.html", context)

@router.get("/new", response_class=HTMLResponse, name="new_post")
async def new_post(request: Request, current_user: User = Depends(get_current_user)):
    context = {
        "current_user": current_user,
        "request": request,
    } 
    context = {
        "current_user": current_user,
        "request": request,
    }
    return templates.TemplateResponse("new_post.html", context)

@router.post("/create", response_class=RedirectResponse, name="create_post")
async def create_post(
    request: Request,
    response: Response,
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tag_list = [tag.strip() for tag in tags.split(',')]
    # Проверяем существование тегов и создаем новые, если не найдены
    tag_objects = []
    for tag_name in tag_list:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag is None:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tag_objects.append(tag)

    new_post = Post(
        title=title,
        content=content,
        author=current_user,
        tags=tag_objects
    )
    db.add(new_post)
    db.commit()
    
    response = RedirectResponse(url="/posts", status_code=status.HTTP_303_SEE_OTHER)
    set_message_cookie(response, "Post created successfully", "success")
    
    return response

@router.get("/{post_id}", response_class=HTMLResponse, name="get_post")
async def get_post(request: Request, post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    context = {
        "current_user": current_user,
        "request": request,
        "post": post
    }
    return templates.TemplateResponse("post.html", {"request": request, "post": post})

@router.get("/{post_id}/edit", response_class=HTMLResponse, name="edit_post")
async def edit_post(request: Request, post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    
        
    context = {
        "current_user": current_user,
        "request": request,
        "post": post
    }
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@router.post("/{post_id}/update", response_class=RedirectResponse, name="update_post")
async def update_post(
    request: Request,
    response: Response,
    post_id: int,
    title: str = Form(...),  # Используем Form для получения данных формы
    content: str = Form(...),
    tags: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    # Обновляем поля поста
    post.title = title
    post.content = content

    # Обработка тегов
    tag_names = [tag_name.strip() for tag_name in tags.split(',')]  # Разделение строки тегов
    
        
    # Проверяем существование тегов и создаем новые, если не найдены
    tag_objects = []
    for tag_name in tag_names:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag is None:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tag_objects.append(tag)
    
    post.tags = [tag for tag in tag_objects if tag]

    db.commit()

    response=RedirectResponse(url=f"/posts/{post_id}", status_code=status.HTTP_303_SEE_OTHER)
    set_message_cookie(response, "Post updated successfully", "success")
    return response

@router.post("/{post_id}/delete", response_class=RedirectResponse, name="delete_post")
async def delete_post(
    request: Request,
    response: Response,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()

    response=RedirectResponse(url="/posts", status_code=status.HTTP_303_SEE_OTHER)
    set_message_cookie(response, "Post deleted successfully", "success")
    return response
