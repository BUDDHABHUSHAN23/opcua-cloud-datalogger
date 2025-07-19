from pydantic import BaseModel
from typing import Optional

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_enabled: bool = True
    schedule_type: Optional[str]
    schedule_details: Optional[str]
    server_id: int
    schedule_mode: Optional[str] = None
    interval: Optional[int] = None
    mode: str  # ✅ Add this line

class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

class GroupOut(GroupBase):
    id: int

    class Config:
        from_attributes = True