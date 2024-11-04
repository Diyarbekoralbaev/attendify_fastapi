from pathlib import Path

import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, WebSocket, WebSocketDisconnect

from manager import manager
from schemas import ClientSchema, ClientVisitHistorySchema
from database import session, engine
from models import ClientsModel, ClientVisitHistoryModel
from datetime import datetime, timedelta
import datetime

client_router = APIRouter(
    tags=['client']
)

session = session(bind=engine)

upload_folder = Path('uploads')
upload_folder.mkdir(parents=True, exist_ok=True)


@client_router.post('/create')
async def create_client(image: UploadFile = File(...), first_seen: str = Form(...), last_seen: str = Form(...),
                        visit_count: int = Form, gender: int = Form, age: int = Form):
    try:
        image_path = upload_folder / image.filename
        async with aiofiles.open(image_path, 'wb') as file:
            await file.write(await image.read())
        new_client = ClientsModel(
            image=str(image_path),
            first_seen=first_seen,
            last_seen=last_seen,
            visit_count=visit_count,
            gender=gender,
            age=age
        )
        session.add(new_client)
        session.commit()

        data = {
            'id': new_client.id,
            'image': str(image_path),
            'first_seen': first_seen,
            'last_seen': last_seen,
            'visit_count': visit_count,
            'gender': gender,
        }
        response_model = {
            'status': 'success',
            'message': 'Client added successfully',
            'data': data
        }
        # Broadcast the new client to all WebSocket connections
        await manager.broadcast({
            'event': 'client_update',
            'data': data
        })

        return response_model
    except Exception as e:
        session.rollback()
        return {'detail': str(e)}


@client_router.get('/clients')
async def get_clients():
    clients = session.query(ClientsModel).all()
    return clients


@client_router.get('/clients/{client_id}')
async def get_client(client_id: int):
    client = session.query(ClientsModel).filter(ClientsModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')
    return client

@client_router.delete('/clients/{client_id}')
async def delete_client(client_id: int):
    try:
        client = session.query(ClientsModel).filter(ClientsModel.id == client_id).first()
        visit_history = session.query(ClientVisitHistoryModel).filter(ClientVisitHistoryModel.client_id == client_id).all()
        if visit_history:
            for visit in visit_history:
                session.delete(visit)
        if not client:
            raise HTTPException(status_code=404, detail='Client not found')
        session.delete(client)
        session.commit()
        await manager.broadcast({
            'event': 'client_delete',
            'data': {'id': client_id}
        })
        return {'status': 'success', 'message': 'Client deleted successfully'}
    except Exception as e:
        session.rollback()
        return {'detail': str(e)}


@client_router.get('/visit-history/')
async def get_all_visit_history(from_date: str = None, to_date: str = None):
    try:
        clients = session.query(ClientVisitHistoryModel).all()
        if from_date:
            clients = clients.filter(ClientVisitHistoryModel.datetime >= from_date)
        if to_date:
            clients = clients.filter(ClientVisitHistoryModel.datetime <= to_date)
        if clients:
            return clients
        raise HTTPException(status_code=404, detail='No visit history found')
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@client_router.post('/visit-history/{client_id}')
async def add_visit_history(history: ClientVisitHistorySchema, client_id: int):
    try:
        client = session.query(ClientsModel).filter(ClientsModel.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail='Client not found')
        client.visit_count += 1
        new_visit = ClientVisitHistoryModel(
            datetime=str(history.datetime),
            device_id=history.device_id,
            client_id=client_id
        )
        session.add(client)
        session.add(new_visit)
        session.commit()

        return new_visit
    except Exception as e:
        session.rollback()
        return {'detail': str(e)}


@client_router.get('/visit-history/{client_id}')
async def get_visit_history(client_id: int):
    visits = session.query(ClientVisitHistoryModel).filter(ClientVisitHistoryModel.client_id == client_id).all()
    if not visits:
        raise HTTPException(status_code=404, detail='Client not found')
    return visits


@client_router.get('/visit-history/{client_id}/{visit_id}')
async def get_visit_history(client_id: int, visit_id: int):
    visit = session.query(ClientVisitHistoryModel).filter(ClientVisitHistoryModel.client_id == client_id,
                                                          ClientVisitHistoryModel.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail='Client not found')
    return visit
