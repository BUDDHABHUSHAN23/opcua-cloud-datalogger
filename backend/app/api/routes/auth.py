from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.user import LoginRequest
from app.services.auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
@router.post("/login/")  # ✅ Accepts with or without slash
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    print(f"🔐 Login attempt: {data.email}")
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token}
