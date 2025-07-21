from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.crud import report_schedule as crud
from app.schemas.report import ReportScheduleCreate, ReportScheduleOut
from datetime import datetime
from app.workers.report_worker import run_report_task

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

@router.post("/run/{schedule_id}")    # This are the changes made to the file
def run_report_now(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud.get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    run_report_task.delay(schedule_id)
    return {"status": "queued", "report_id": schedule_id, "name": schedule.name}

