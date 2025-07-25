from sqlalchemy.orm import Session
from app.db.models.group import Group
from app.schemas.group import GroupCreate

def create_group(db: Session, group: GroupCreate) -> Group:
    db_group = Group(
        name=group.name,
        server_id=group.server_id,
        mode=group.mode,
        interval=group.interval,
        schedule_type=group.schedule_type,
        schedule_details=group.schedule_details
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_all_groups(db: Session):
    return db.query(Group).all()

def update_group(db: Session, group_id: int, group_data: dict):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        return None
    for key, value in group_data.items():
        setattr(db_group, key, value)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        return None
    db.delete(db_group)
    db.commit()
    return db_group

def get_group_by_id(db: Session, group_id: int) -> Group:
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        return None
    return db_group
