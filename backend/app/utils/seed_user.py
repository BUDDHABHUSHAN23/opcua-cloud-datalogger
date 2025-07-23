
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.db.database import SessionLocal
from app.db.models.user import User
from app.utils.security import hash_password

def seed_admin():
    db = SessionLocal()
    if not db.query(User).filter(User.email == "admin@example.com").first():
        user = User(email="admin@example.com", hashed_password=hash_password("admin123"))
        db.add(user)
        db.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin already exists.")

if __name__ == "__main__":
    seed_admin()
