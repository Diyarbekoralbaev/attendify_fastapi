from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmployeeAttendanceSchema(BaseModel):
    employee_id: int
    device_id: int
    image: str
    image: Optional[str]
    timestamp: str
    score: float
