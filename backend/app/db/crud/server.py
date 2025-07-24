# backend/app/db/crud/server.py

from sqlalchemy.orm import Session
from app.db.models.server import Server
from typing import Optional


# This to get all servers from the database
def get_all_servers(db: Session):
    return db.query(Server).all()

# This is to add a new server to the database
def add_server(db: Session, name: str, endpoint_url: str):
    existing = db.query(Server).filter((Server.name == name) | (Server.endpoint_url == endpoint_url)).first()
    if existing:
        raise Exception("Server with same name or endpoint already exists.")
    new_server = Server(name=name, endpoint_url=endpoint_url)
    db.add(new_server)
    db.commit()
    db.refresh(new_server)
    return new_server

# This is to delete a server from the database
def delete_server(db: Session, server_id: int):
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise Exception("Server not found")
    db.delete(server)
    db.commit()

# This is to get a server by its ID from the database
def get_server_by_id(db: Session, server_id: int) -> Optional[Server]:
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise Exception("Server not found")
    return server


