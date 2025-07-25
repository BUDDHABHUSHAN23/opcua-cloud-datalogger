from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.crud import group as crud
from app.schemas.group import GroupCreate, GroupUpdate, GroupOut

router = APIRouter()

@router.get("/", response_model=List[GroupOut])
def list_groups(db: Session = Depends(get_db)):
    return crud.get_all_groups(db)

@router.post("/", response_model=GroupOut, status_code=201)
def create_group(payload: GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, payload)   # changed to use GroupCreate schema

@router.put("/{group_id}", status_code=200)
def update_group(group_id: int, payload: GroupUpdate, db: Session = Depends(get_db)):
    crud.update_group(db, group_id, payload.dict())
    return {"detail": "Group updated"}

@router.delete("/{group_id}", status_code=200)
def remove_group(group_id: int, db: Session = Depends(get_db)):
    crud.delete_group(db, group_id)
    return {"detail": "Group and associated tags deleted"}

@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group    