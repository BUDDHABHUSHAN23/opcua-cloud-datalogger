# group model

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.database import Base

class Group(Base):
    __tablename__ = "logging_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_enabled = Column(Boolean, default=True)
    schedule_type = Column(String)
    schedule_details = Column(String)
    server_id = Column(Integer, ForeignKey("servers.id"))