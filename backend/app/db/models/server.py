# server model

from sqlalchemy import Column, Integer, String
from app.db.database import Base



class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    endpoint_url = Column(String, unique=True, nullable=False)