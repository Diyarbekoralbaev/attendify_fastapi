from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ClientSchema(BaseModel):
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]
    visit_count: Optional[int]
    gender: Optional[int]
    age: Optional[int]


class ClientVisitHistorySchema(BaseModel):
    datetime: str
    device_id: Optional[int]