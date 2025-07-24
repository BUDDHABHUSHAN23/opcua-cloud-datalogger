from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    endpoint_url = Column(String, unique=True, nullable=False)  # ✅ Correct

    # ✅ Add this line
    tags = relationship("Tag", back_populates="server")
