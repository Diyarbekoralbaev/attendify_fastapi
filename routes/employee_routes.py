from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import shutil
import aiofiles
from pathlib import Path
from database import session, engine
from manager import manager
from models import EmployeeModel
from schemas import EmployeeSchema
from typing import Optional

employee_router = APIRouter(
    tags=['employee']
)

session = session(bind=engine)

upload_folder = Path('uploads')
upload_folder.mkdir(parents=True, exist_ok=True)



@employee_router.post('/create')
async def create_employee(image: UploadFile = File(...), name: str = Form(...), email: str = Form(...),
                          phone: str = Form(...), department_id: int = Form(...)):
    image_path = upload_folder / image.filename
    async with aiofiles.open(image_path, 'wb') as file:
        await file.write(await image.read())
    # check for unique fields
    if session.query(EmployeeModel).filter(EmployeeModel.email == email).first():
        raise HTTPException(status_code=400, detail='Email already exists')
    if session.query(EmployeeModel).filter(EmployeeModel.phone == phone).first():
        raise HTTPException(status_code=400, detail='Phone number already exists')
    try:
        new_employee = EmployeeModel(
            name=name,
            email=email,
            phone=phone,
            image=str(image_path),
            department_id=department_id
        )
        session.add(new_employee)
        session.commit()
        data = {
            'id': new_employee.id,
            'name': name,
            'email': email,
            'phone': phone,
            'image': str(image_path),
            'department_id': department_id
        }
        response_model = {
            'status': 'success',
            'message': 'Employee added successfully',
            'data': data
        }

        await manager.broadcast({
            'event': 'employee_update',
            'data': data
        })

        return response_model
    except Exception as e:
        session.rollback()
        return {'detail': str(e)}


@employee_router.get('/employees')
async def get_employees():
    employees = session.query(EmployeeModel).all()
    return employees


@employee_router.get('/employees/{employee_id}')
async def get_employee(employee_id: int):
    employee = session.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    return employee


@employee_router.put('/employees/{employee_id}')
async def update_employee(
        employee_id: int,
        image: Optional[UploadFile] = File(None),
        name: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        department_id: Optional[int] = Form(None)
):
    db_employee = session.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail='Employee not found')

    # Update fields only if they are provided
    if image:
        image_path = upload_folder / image.filename
        async with aiofiles.open(image_path, 'wb') as file:
            await file.write(await image.read())
        db_employee.image = str(image_path)

    if name is not None:
        db_employee.name = name

    if email is not None:
        db_employee.email = email

    if phone is not None:
        db_employee.phone = phone

    # if working_graphic_id is not None:
    #     db_employee.working_graphic_id = working_graphic_id

    if department_id is not None:
        db_employee.department_id = department_id

    session.commit()

    data = {
        'name': db_employee.name,
        'email': db_employee.email,
        'phone': db_employee.phone,
        'image': db_employee.image,
        # 'working_graphic_id': db_employee.working_graphic_id,
        'department_id': db_employee.department_id
    }

    response_model = {
        'status': 'success',
        'message': 'Employee updated successfully',
        'data': data
    }

    return response_model


@employee_router.delete('/employees/{employee_id}')
async def delete_employee(employee_id: int):
    db_employee = session.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    session.delete(db_employee)
    session.commit()
    await manager.broadcast({
        'event': 'employee_delete',
        'data': {'id': employee_id}
    })
    return {'message': 'Employee deleted successfully'}
