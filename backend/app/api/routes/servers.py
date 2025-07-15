# servers route
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import server as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_servers(db: Session = Depends(get_db)):
    return crud.get_all_servers(db)

@router.post("/")
def create_server(name: str, endpoint_url: str, db: Session = Depends(get_db)):
    return crud.add_server(db, name, endpoint_url)

@router.delete("/{server_id}")
def remove_server(server_id: int, db: Session = Depends(get_db)):
    crud.delete_server(db, server_id)
    return {"detail": "Server deleted"}