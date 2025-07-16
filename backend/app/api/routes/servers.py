# backend/app/api/routes/servers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal
from app.db.crud import server as crud
from app.db.models.server import Server
from app.schemas.server import ServerCreate, ServerOut  # Make sure these are defined

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ServerOut])
def list_servers(db: Session = Depends(get_db)):
    """List all OPC UA servers"""
    try:
        servers = db.query(Server).all()
        return servers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ServerOut)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    """Create new OPC UA server"""
    try:
        return crud.add_server(db, server.name, server.endpoint_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{server_id}")
def remove_server(server_id: int, db: Session = Depends(get_db)):
    """Delete server by ID"""
    crud.delete_server(db, server_id)
    return {"detail": "Server deleted"}
