from sqlalchemy.orm import Session
from app.db.models.group import Group

def create_group(db: Session, group_data: dict):
    group = Group(**group_data)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def get_all_groups(db: Session):
    return db.query(Group).all()
