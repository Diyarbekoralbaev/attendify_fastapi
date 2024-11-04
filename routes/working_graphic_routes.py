from pathlib import Path

import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, WebSocket, WebSocketDisconnect

from manager import manager
from schemas import WorkingGraphicSchema
from database import session, engine
from models import WorkingGraphicModel
from datetime import datetime, timedelta
from sqlalchemy import func


working_graphic_router = APIRouter(
    tags=['working_graphic']
)

session = session(bind=engine)

upload_folder = Path('uploads')


# Create working graphic
@working_graphic_router.post('/', response_model=WorkingGraphicSchema, response_model_exclude_none=True, status_code=201)
async def create_working_graphic(working_graphic: WorkingGraphicSchema):
    working_graphic = WorkingGraphicModel(**working_graphic.dict())
    session.add(working_graphic)
    session.commit()
    return working_graphic


# Get working graphic by id
@working_graphic_router.get('/{working_graphic_id}', response_model=WorkingGraphicSchema, response_model_exclude_none=True)
async def get_working_graphic(working_graphic_id: int):
    working_graphic = session.query(WorkingGraphicModel).filter_by(id=working_graphic_id).first()
    if not working_graphic:
        raise HTTPException(status_code=404, detail='Working graphic not found')
    return working_graphic


# Update working graphic by id
@working_graphic_router.put('/{working_graphic_id}', response_model=WorkingGraphicSchema, response_model_exclude_none=True)
async def update_working_graphic(working_graphic_id: int, working_graphic: WorkingGraphicSchema):
    working_graphic = session.query(WorkingGraphicModel).filter_by(id=working_graphic_id).first()
    if not working_graphic:
        raise HTTPException(status_code=404, detail='Working graphic not found')
    working_graphic.update(working_graphic.dict())
    session.commit()
    return working_graphic


# Delete working graphic by id
@working_graphic_router.delete('/{working_graphic_id}', status_code=204)
async def delete_working_graphic(working_graphic_id: int):
    working_graphic = session.query(WorkingGraphicModel).filter_by(id=working_graphic_id).first()
    if not working_graphic:
        raise HTTPException(status_code=404, detail='Working graphic not found')
    session.delete(working_graphic)
    session.commit()
    return working_graphic


# Get all working graphics
@working_graphic_router.get('/', response_model=list[WorkingGraphicSchema])
async def get_all_working_graphics():
    working_graphics = session.query(WorkingGraphicModel).all()
    return working_graphics
