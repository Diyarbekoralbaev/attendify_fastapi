# models/employee_model.py
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import Base


class EmployeeModel(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    email = Column(String(70), unique=True)
    image = Column(Text, nullable=False)
    phone = Column(String(15), unique=True)
    is_active = Column(Boolean, default=True)
    # working_graphic_id = Column(Integer, ForeignKey('working_graphic.id'))
    department_id = Column(Integer, ForeignKey('department.id'))

    def __repr__(self):
        return f"<Employee {self.name}>"
