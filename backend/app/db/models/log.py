from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base
from datetime import datetime

class LogData(Base):
    __tablename__ = "log_data"
    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(String)
    status_code = Column(String)