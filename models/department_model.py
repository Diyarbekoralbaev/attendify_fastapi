# models/department_model.py
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class DepartmentModel(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255), nullable=True)