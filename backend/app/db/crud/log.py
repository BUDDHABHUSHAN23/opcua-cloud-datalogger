from sqlalchemy.orm import Session
from app.db.models.log import LogData
from datetime import datetime
from sqlalchemy import text  # ✅ Add this

def log_data(db: Session, records: list):
    if records:
        db.bulk_insert_mappings(LogData, records)
        db.commit()

#updated to fetch historical data

def get_historical_data(db: Session, group_id: int, start: datetime, end: datetime):
    return db.execute(
        text(
            """
            SELECT log_data.timestamp, tags.alias, tags.node_id, log_data.value
            FROM log_data
            JOIN tags ON tags.id = log_data.tag_id
            WHERE tags.group_id = :group_id
            AND log_data.timestamp BETWEEN :start AND :end
            ORDER BY log_data.timestamp
            """
        ),
        {"group_id": group_id, "start": start, "end": end},
    ).fetchall()
