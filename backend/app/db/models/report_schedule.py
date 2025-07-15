from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db.database import Base

class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("logging_groups.id"))
    output_folder = Column(String)
    report_format = Column(String)
    template_path = Column(String)
    schedule_type = Column(String)
    is_enabled = Column(Boolean, default=True)
    last_run_timestamp = Column(DateTime, nullable=True)