from fastapi import APIRouter
import shutil
import aiofiles
from pathlib import Path

from setuptools.command.build_ext import if_dl

from database import session, engine
from models import DepartmentModel
from schemas import DepartmentSchema
from typing import Optional

session = session(bind=engine)


department_router = APIRouter(
    tags=["department"],
)


@department_router.post("/department", response_model=DepartmentSchema)
async def create_department(department: DepartmentSchema):
    try:
        new_department = DepartmentModel(name=department.name, description=department.description)
        session.add(new_department)
        session.commit()
        return new_department
    except Exception as e:
        session.rollback()
        return {"detail": str(e)}


@department_router.get("/department", response_model=list[DepartmentSchema])
async def get_departments():
    try:
        departments = session.query(DepartmentModel).all()
        if departments:
            return departments
        return {"detail": "No departments found"}
    except Exception as e:
        return {"detail": str(e)}

@department_router.get("/department/{department_id}", response_model=DepartmentSchema)
async def get_department(department_id: int):
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
        if department:
            return department
        return {"detail": "Department not found"}
    except Exception as e:
        return {"detail": str(e)}



@department_router.put("/department/{department_id}", response_model=DepartmentSchema)
async def update_department(department_id: int, department: DepartmentSchema):
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
        if department:
            department.name = department.name
            department.description = department.description
            session.commit()
            return department
        return {"detail": "Department not found"}
    except Exception as e:
        session.rollback()
        return {"detail": str(e)}

@department_router.delete("/department/{department_id}")
async def delete_department(department_id: int):
    try:
        department = session.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
        if department:
            session.delete(department)
            session.commit()
            return {"detail": "Department deleted"}
        return {"detail": "Department not found"}
    except Exception as e:
        session.rollback()
        return {"detail": str(e)}
