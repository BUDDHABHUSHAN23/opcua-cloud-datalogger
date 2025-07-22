# tag CRUD

from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.db.models.tag import Tag

def get_tags_for_group(db: Session, group_id: int):
    return db.query(Tag).filter(Tag.group_id == group_id).all()

# this will save the tags to the database
def save_tags(db: Session, group_id: int, tags: list):
    created = []
    for tag in tags:
        # Check if alias already exists
        existing = db.query(Tag).filter_by(alias=tag["alias"]).first()
        if existing:
            continue

        new_tag = Tag(**tag, group_id=group_id)
        db.add(new_tag)
        created.append(new_tag.alias)

    db.commit()
    return True, f"{len(created)} tag(s) saved"
