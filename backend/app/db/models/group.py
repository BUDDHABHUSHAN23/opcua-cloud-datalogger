# group model

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Group(Base):
    __tablename__ = "logging_groups"
    __table_args__ = {'extend_existing': True}  # ✅ add this line   # to allow redefinition
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    is_enabled = Column(Boolean, default=True)
    schedule_type = Column(String)
    schedule_details = Column(String)
    schedule_mode = Column(String, nullable=True)
    server_id = Column(Integer, ForeignKey("servers.id"))

    # Optional enhancement:
    tags = relationship("Tag", back_populates="group", cascade="all, delete")
