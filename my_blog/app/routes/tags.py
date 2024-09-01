from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.security import  get_current_user
from app.models import Tag, User, get_db

router = APIRouter()

class TagCreate(BaseModel):
    name: str

@router.get("/")
async def get_tags(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags

@router.post("/")
async def create_tag(tag: TagCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")

    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    db.commit()
    return {"msg": "Tag created successfully"}

@router.get("/{tag_id}")
async def get_tag(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

class TagUpdate(BaseModel):
    name: str

@router.put("/{tag_id}")
async def update_tag(tag_id: int, tag_update: TagUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = tag_update.name
    db.commit()
    return {"msg": "Tag updated successfully"}

@router.delete("/{tag_id}")
async def delete_tag(tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"msg": "Tag deleted successfully"}
