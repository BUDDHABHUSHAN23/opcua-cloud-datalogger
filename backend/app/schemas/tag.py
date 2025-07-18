from pydantic import BaseModel, Field
from typing import Optional

class TagBase(BaseModel):
    alias: str = Field(..., min_length=1)
    node_id: str
    data_type: Optional[str] = "float"

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    group_id: int

    class Config:
        from_attributes = True
        