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
