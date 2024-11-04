from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    name: str
    description: Optional[str]
    is_active: Optional[bool] = True
