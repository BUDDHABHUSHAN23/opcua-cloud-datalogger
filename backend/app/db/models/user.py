from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# this is going to be used for user roles and permissions
# class User(Base):
#     id: int
#     name: str
#     email: str
#     role: str  # "admin", "operator", "viewer"
#     hashed_password: str
#     is_active: bool
