from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.crud import report_schedule as crud
from app.schemas.report import ReportScheduleCreate, ReportScheduleOut
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[ReportScheduleOut])
def list_schedules(db: Session = Depends(get_db)):
    return crud.get_all_schedules(db)

@router.post("/", response_model=ReportScheduleOut, status_code=201)
def create_schedule(payload: ReportScheduleCreate, db: Session = Depends(get_db)):
    return crud.add_schedule(db, payload.dict())

@router.put("/{schedule_id}/last_run")
def update_last_run(schedule_id: int, ts: datetime, db: Session = Depends(get_db)):
    crud.update_last_run(db, schedule_id, ts)
    return {"detail": "Last run updated"}

@router.delete("/{schedule_id}", status_code=200)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    crud.delete_schedule(db, schedule_id)
    return {"detail": "Schedule deleted"}