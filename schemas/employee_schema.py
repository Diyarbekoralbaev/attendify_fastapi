from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    name: str
    email: str
    phone: str
    image: str
    is_active: Optional[bool] = True
    # working_graphic_id: int
    department_id: int