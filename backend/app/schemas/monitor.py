from pydantic import BaseModel
from typing import Any, List

class TagValue(BaseModel):
    alias: str
    value: Any
    quality: str

class MonitoringPayload(BaseModel):
    timestamp: str
    values: List[TagValue]