from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True)
    node_id = Column(String, nullable=False)
    data_type = Column(String)
    group_id = Column(Integer, ForeignKey("logging_groups.id"))

    # ✅ Use class name only (no full module path)
    group = relationship("Group", back_populates="tags")
