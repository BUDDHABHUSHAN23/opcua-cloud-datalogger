from pydantic import BaseModel
from typing import Optional

class GroupBase(BaseModel):      # USED in GroupCreate and GroupUpdate
    """Base schema for Group."""
    name: str
    description: Optional[str] = None
    is_enabled: bool = True
    schedule_type: Optional[str]
    schedule_details: Optional[str]
    server_id: int
    schedule_mode: Optional[str] = None
    interval: Optional[int] = None
    mode: str  # ✅ Add this line

class GroupCreate(GroupBase):      # USED in GroupCreate
    """Schema for Group creation."""
    pass

class GroupUpdate(GroupBase):      # USED in GroupUpdate
    """Schema for Group update."""
    pass

class GroupOut(GroupBase):        # USED in GroupOut
    """Schema for Group output."""
    id: int

    class Config:                 # USED in GroupOut
        """Pydantic configuration."""
        from_attributes = True

        