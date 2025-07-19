# tag CRUD

from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.db.models.tag import Tag

def get_tags_for_group(db: Session, group_id: int):
    return db.query(Tag).filter(Tag.group_id == group_id).all()

def save_tags(db: Session, group_id: int, tags: List[Dict]) -> Tuple[bool, str]:
    try:
        db.query(Tag).filter(Tag.group_id == group_id).delete()
        for tag in tags:
            db.add(Tag(**tag, group_id=group_id))
        db.commit()
        return True, "Tags saved"
    except Exception as e:
        db.rollback()
        return False, str(e)
