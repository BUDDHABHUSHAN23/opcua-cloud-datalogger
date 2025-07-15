# groups route
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import group as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_groups(db: Session = Depends(get_db)):
    return crud.get_all_groups(db)

@router.post("/")
def create_group(payload: dict, db: Session = Depends(get_db)):
    return crud.add_group(db, **payload)

@router.put("/{group_id}")
def update_group(group_id: int, payload: dict, db: Session = Depends(get_db)):
    crud.update_group(db, group_id, **payload)
    return {"detail": "Group updated"}

@router.delete("/{group_id}")
def remove_group(group_id: int, db: Session = Depends(get_db)):
    crud.delete_group(db, group_id)
    return {"detail": "Group deleted"}