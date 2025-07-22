from pydantic import BaseModel, Field
from typing import Optional

class TagBase(BaseModel):
    alias: str = Field(..., min_length=1)
    node_id: str
    data_type: Optional[str] = "float"

class TagCreate(TagBase):
    server_id: int
    node_id: str
    alias: str
    data_type: Optional[str] = None
    mode: Optional[str] = "read"
    sampling_rate: Optional[int] = 5
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    enabled: Optional[bool] = True
    pass

class TagOut(TagBase):
    id: int
    group_id: int

    class Config:
        from_attributes = True
        