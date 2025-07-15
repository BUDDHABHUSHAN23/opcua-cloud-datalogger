# group CRUD
from sqlalchemy.orm import Session
from app.db.models.group import Group

def get_all_groups(db: Session):
    return db.query(Group).all()

def add_group(db: Session, **kwargs):
    group = Group(**kwargs)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def update_group(db: Session, group_id: int, **kwargs):
    db.query(Group).filter(Group.id == group_id).update(kwargs)
    db.commit()

def delete_group(db: Session, group_id: int):
    db.query(Group).filter(Group.id == group_id).delete()
    db.commit()