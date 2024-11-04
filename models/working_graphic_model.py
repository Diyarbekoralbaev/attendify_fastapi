# models/work_graphic_model.py
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import Base


class WorkingGraphicModel(Base):
    __tablename__ = "working_graphic"
    id = Column(Integer, primary_key=True)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    is_active = Column(Boolean, default=True)
