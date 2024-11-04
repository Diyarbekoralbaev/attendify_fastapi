# schemas/working_graphic_schema.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WorkingGraphicSchema(BaseModel):
    id: Optional[int]
    start_date: datetime
    end_date: datetime
    is_active: bool