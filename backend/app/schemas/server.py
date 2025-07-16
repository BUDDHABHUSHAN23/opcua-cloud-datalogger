# backend/app/schemas/server.py

from pydantic import BaseModel


class ServerBase(BaseModel):
    name: str
    endpoint_url: str


class ServerCreate(ServerBase):
    pass


class ServerOut(ServerBase):
    id: int

    class Config:
        from_attributes = True  # replaces deprecated orm_mode
