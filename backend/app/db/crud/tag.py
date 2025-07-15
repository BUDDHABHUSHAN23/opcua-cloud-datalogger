# tag CRUD
from sqlalchemy.orm import Session
from app.db.models.tag import Tag

def get_tags_for_group(db: Session, group_id: int):
    return db.query(Tag).filter(Tag.group_id == group_id).all()

def save_tags(db: Session, group_id: int, tag_list: list):
    db.query(Tag).filter(Tag.group_id == group_id).delete()
    for tag in tag_list:
        db.add(Tag(**tag, group_id=group_id))
    db.commit()
