# tags route
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import tag as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{group_id}")
def list_tags(group_id: int, db: Session = Depends(get_db)):
    return crud.get_tags_for_group(db, group_id)

@router.post("/{group_id}")
def save_tags(group_id: int, tags: list, db: Session = Depends(get_db)):
    crud.save_tags(db, group_id, tags)
    return {"detail": "Tags saved"}
