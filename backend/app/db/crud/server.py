# server CRUD
from sqlalchemy.orm import Session
from app.db.models.server import Server

def get_all_servers(db: Session):
    return db.query(Server).all()

def add_server(db: Session, name: str, endpoint_url: str):
    server = Server(name=name, endpoint_url=endpoint_url)
    db.add(server)
    db.commit()
    db.refresh(server)
    return server

def delete_server(db: Session, server_id: int):
    db.query(Server).filter(Server.id == server_id).delete()
    db.commit()
