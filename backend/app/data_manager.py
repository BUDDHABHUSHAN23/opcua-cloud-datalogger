# app/data_manager.py

from app.db.database import SessionLocal
from app.db.models.group import Group
from app.db.models.tag import Tag
from app.db.models.server import Server
from app.db.models.report_schedule import Report
from app.db.models.log import LogData

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_all_logging_groups():
    db = SessionLocal()
    try:
        return db.query(Group).filter(Group.is_active == True).all()
    finally:
        db.close()


def get_tags_for_group(group_id: int):
    db = SessionLocal()
    try:
        return db.query(Tag).filter(Tag.group_id == group_id).all()
    finally:
        db.close()

def get_server_url(server_id: int):
    db = SessionLocal()
    try:
        server = db.query(Server).filter(Server.id == server_id).first()
        return server.endpoint_url if server else None
    finally:
        db.close()

def log_data_to_db(tag_id: int, value: float, status: str, timestamp: datetime):
    db = SessionLocal()
    try:
        db.add(LogData(tag_id=tag_id, value=value, status=status, timestamp=timestamp))
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log data to DB for tag {tag_id}: {e}")
    finally:
        db.close()

def update_report_last_run(report_id: int):
    db = SessionLocal()
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        if report:
            report.last_run = datetime.utcnow()
            db.commit()
    finally:
        db.close()
