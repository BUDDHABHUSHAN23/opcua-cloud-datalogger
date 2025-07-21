# app/db/crud/report.py

from sqlalchemy.orm import Session
from app.db.models.report_schedule import ReportSchedule
from datetime import datetime

def get_all_schedules(db: Session):
    return db.query(ReportSchedule).all()

def get_schedule_by_id(db: Session, schedule_id: int):
    return db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).first()

def update_report_last_run(db: Session, schedule_id: int, ts: datetime):
    db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).update({"last_run_timestamp": ts})
    db.commit()

def add_schedule(db: Session, data: dict):
    schedule = ReportSchedule(**data)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

def delete_schedule(db: Session, schedule_id: int):
    db.query(ReportSchedule).filter(ReportSchedule.id == schedule_id).delete()
    db.commit()
