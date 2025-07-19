# tag model
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship  # ⬅️ Add this

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True)
    node_id = Column(String, nullable=False)
    data_type = Column(String)
    group_id = Column(Integer, ForeignKey("logging_groups.id"))

        # 🔧 Add this line
    group = relationship("Group", back_populates="tags")