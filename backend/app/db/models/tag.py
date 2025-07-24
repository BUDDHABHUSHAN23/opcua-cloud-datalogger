from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True, nullable=False)
    node_id = Column(String, nullable=False)
    data_type = Column(String)
    mode = Column(String)
    sampling_rate = Column(Integer)
    min_value = Column(Float, default=0)
    max_value = Column(Float, default=0)
    enabled = Column(Boolean, default=True)

    group_id = Column(Integer, ForeignKey("logging_groups.id"))
    server_id = Column(Integer, ForeignKey("servers.id"))  # ✅ NEW FIELD

    # Relationships
    group = relationship("Group", back_populates="tags")
    server = relationship("Server", back_populates="tags")  # Optional
