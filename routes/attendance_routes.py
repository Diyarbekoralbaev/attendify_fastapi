from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from database import session, engine
from models import EmployeeAttendanceModel
from manager import manager


attendance_router = APIRouter(
    tags=['attendance']
)

session = session(bind=engine)

upload_folder = Path('uploads')

upload_folder.mkdir(parents=True, exist_ok=True)


@attendance_router.post('/create')
async def create_attendance(employee_id: int = Form(...), device_id: int = Form(...), image: UploadFile = File(...),
                            timestamp: str = Form(...), score: Optional[float] = Form(0.0)):
    image_path = upload_folder / image.filename
    async with aiofiles.open(image_path, 'wb') as file:
        await file.write(await image.read())
    new_attendance = EmployeeAttendanceModel(
        employee_id=employee_id,
        device_id=device_id,
        image=str(image_path),
        timestamp=timestamp,
        score=score
    )
    session.add(new_attendance)
    session.commit()
    data = {
        'employee_id': employee_id,
        'device_id': device_id,
        'image': str(image_path),
        'timestamp': timestamp,
        'score': score
    }
    response_model = {
        'status': 'success',
        'message': 'Attendance added successfully',
        'data': data
    }

    await manager.broadcast({
        'event': 'new_attendance',
        'data': data
    })

    return response_model


@attendance_router.get('/attendances')
async def get_attendances():
    attendances = session.query(EmployeeAttendanceModel).all()
    return attendances


@attendance_router.get('/attendances/{user_id}')
async def get_attendance(user_id: int):
    attendance = session.query(EmployeeAttendanceModel).filter(EmployeeAttendanceModel.employee_id == user_id).all()
    if not attendance:
        raise HTTPException(status_code=404, detail='Attendance not found')
    return attendance


# @attendance_router.put('/attendances/{attendance_id}')
# async def update_attendance(attendance_id: int, employee_id: int = Form(...), device_id: int = Form(...),
#                             image: UploadFile = File(...), timestamp: str = Form(...), score: Optional[float] = Form(0.0)):
#     attendance = session.query(EmployeeAttendanceModel).filter(EmployeeAttendanceModel.id == attendance_id).first()
#     if not attendance:
#         raise HTTPException(status_code=404, detail='Attendance not found')
#     image_path = upload_folder / image.filename
#     async with aiofiles.open(image_path, 'wb') as file:
#         await file.write(await image.read())
#     attendance.employee_id = employee_id if employee_id else attendance.employee_id
#     attendance.device_id = device_id if device_id else attendance.device_id
#     attendance.image = str(image_path) if image else attendance.image
#     attendance.timestamp = timestamp if timestamp else attendance.timestamp
#     attendance.score = score if score else attendance.score
#     session.commit() # Save the changes
#     data = {
#         'employee_id': employee_id,
#         'device_id': device_id,
#         'image': str(image_path),
#         'timestamp': timestamp,
#         'score': score
#     }
#     response_model = {
#         'status': 'success',
#         'message': 'Attendance updated successfully',
#         'data': data
#     }
#     return response_model



@attendance_router.delete('/attendances/{attendance_id}')
async def delete_attendance(attendance_id: int):
    attendance = session.query(EmployeeAttendanceModel).filter(EmployeeAttendanceModel.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail='Attendance not found')
    session.delete(attendance)
    session.commit()
    return {'status': 'success', 'message': 'Attendance deleted successfully'}
