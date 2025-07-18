from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.crud import tag as crud
from app.schemas.tag import TagCreate, TagOut

router = APIRouter()

@router.get("/{group_id}", response_model=List[TagOut])
def list_tags(group_id: int, db: Session = Depends(get_db)):
    return crud.get_tags_for_group(db, group_id)

@router.post("/{group_id}", status_code=201)
def save_tags(group_id: int, tags: List[TagCreate], db: Session = Depends(get_db)):
    success, message = crud.save_tags(db, group_id, [t.dict() for t in tags])
    if not success:
        raise HTTPException(status_code=409, detail=message)
    return {"detail": message}