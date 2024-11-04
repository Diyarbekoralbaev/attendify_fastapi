# models/attendance_model.py
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from database import Base
from datetime import datetime


class EmployeeAttendanceModel(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    device_id = Column(Integer)
    image = Column(Text, nullable=False)
    timestamp = Column(String(80), nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(String(80), nullable=False, default=datetime.now())
