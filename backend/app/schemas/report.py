from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReportScheduleBase(BaseModel):
    name: str
    group_id: int
    output_folder: str
    report_format: str
    template_path: str
    schedule_type: str
    is_enabled: Optional[bool] = True

class ReportScheduleCreate(ReportScheduleBase):
    pass

class ReportScheduleOut(ReportScheduleBase):
    id: int
    last_run_timestamp: Optional[datetime]

    class Config:
        from_attributes = True