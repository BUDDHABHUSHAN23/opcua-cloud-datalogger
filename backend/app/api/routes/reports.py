# reports route
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import report_schedule as crud
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_schedules(db: Session = Depends(get_db)):
    return crud.get_all_schedules(db)

@router.post("/")
def create_schedule(payload: dict, db: Session = Depends(get_db)):
    return crud.add_schedule(db, **payload)

@router.put("/{schedule_id}/last_run")
def update_last_run(schedule_id: int, ts: datetime, db: Session = Depends(get_db)):
    crud.update_last_run(db, schedule_id, ts)
    return {"detail": "Last run updated"}

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    crud.delete_schedule(db, schedule_id)
    return {"detail": "Schedule deleted"}