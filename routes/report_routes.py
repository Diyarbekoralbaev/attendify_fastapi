from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, WebSocket, WebSocketDisconnect
from io import BytesIO

from sqlalchemy.orm import Query

from manager import manager
from schemas import ClientSchema, ClientVisitHistorySchema
from database import session, engine
from models import ClientsModel, ClientVisitHistoryModel, EmployeeModel, EmployeeAttendanceModel
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd
from enum import Enum
from fastapi import Query
from fastapi.responses import Response

report_router = APIRouter(
    tags=['report']
)

session = session(bind=engine)

upload_folder = Path('uploads')
upload_folder.mkdir(parents=True, exist_ok=True)


# Daily new clients
@report_router.get('/daily-new-clients')
async def get_daily_new_clients():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= today_start
    ).all()
    return clients


# Daily returning clients
@report_router.get('/daily-returning-clients')
async def get_daily_returning_clients():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.last_seen, 'YYYY-MM-DD HH24:MI:SS') >= today_start
    ).filter(
        ClientsModel.visit_count > 1
    ).all()
    return clients


# Weekly new clients
@report_router.get('/weekly-new-clients')
async def get_weekly_new_clients():
    today = datetime.now()
    start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_week
    ).all()
    return clients


# Weekly returning clients
@report_router.get('/weekly-returning-clients')
async def get_weekly_returning_clients():
    today = datetime.now()
    start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.last_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_week
    ).filter(
        ClientsModel.visit_count > 1
    ).all()
    return clients


# Monthly new clients
@report_router.get('/monthly-new-clients')
async def get_monthly_new_clients():
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_month
    ).all()
    return clients


# Monthly returning clients
@report_router.get('/monthly-returning-clients')
async def get_monthly_returning_clients():
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_month
    ).filter(
        ClientsModel.visit_count > 1
    ).all()
    return clients


# Export daily new clients
@report_router.get('/export/daily-new-clients')
async def export_daily_new_clients(format: str = Query("xlsx", enum=["csv", "xlsx"])):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= today_start
    ).all()

    df = pd.DataFrame([client.to_dict() for client in clients])
    output = BytesIO()

    if format == "xlsx":
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Daily New Clients")
        output.seek(0)
        headers = {
            'Content-Disposition': f'attachment; filename=daily_new_clients_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        }
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif format == "csv":
        df.to_csv(output, index=False)
        output.seek(0)
        headers = {
            'Content-Disposition': f'attachment; filename=daily_new_clients_{datetime.now().strftime("%Y-%m-%d")}.csv'
        }
        media_type = 'text/csv'
    else:
        raise HTTPException(status_code=400, detail="Invalid format specified.")

    # Return the in-memory file as a response
    return Response(content=output.getvalue(), media_type=media_type, headers=headers)


# Export daily returning clients
@report_router.get('/export/daily-returning-clients')
async def export_daily_returning_clients():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.last_seen, 'YYYY-MM-DD HH24:MI:SS') >= today_start
    ).filter(
        ClientsModel.visit_count > 1
    ).all()

    df = pd.DataFrame([client.to_dict() for client in clients])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=f'Daily Returning Clients {today_start.strftime("%Y-%m-%d")}')
    output.seek(0)

    # Return the in-memory Excel file as a response
    headers = {
        'Content-Disposition': f'attachment; filename=daily_returning_clients_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    }
    return Response(
        content=output.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers
    )


# Export weekly new clients
@report_router.get('/export/weekly-new-cllients')
async def export_weekly_new_clients():
    today = datetime.now()
    start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_week
    ).all()

    df = pd.DataFrame([client.to_dict() for client in clients])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=f'Weekly New Clients {start_of_week.strftime("%Y-%m-%d")}')
    output.seek(0)

    # Return the in-memory Excel file as a response
    headers = {
        'Content-Disposition': f'attachment; filename=weekly_new_clients_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    }
    return Response(
        content=output.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers
    )


# Export weekly returning clients
@report_router.get('/export/weekly-returning-clients')
async def export_weekly_returning_clients():
    today = datetime.now()
    start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.last_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_week
    ).filter(
        ClientsModel.visit_count > 1
    ).all()

    df = pd.DataFrame([client.to_dict() for client in clients])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=f'Weekly Returning Clients {start_of_week.strftime("%Y-%m-%d")}')
    output.seek(0)

    # Return the in-memory Excel file as a response
    headers = {
        'Content-Disposition': f'attachment; filename=weekly_returning_clients_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    }
    return Response(
        content=output.getvalue(),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers
    )


# Export monthly new clients
@report_router.get('/export/monthly-new-clients')
async def export_monthly_new_clients(format: str = Query("xlsx", enum=["csv", "xlsx"])):
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    clients = session.query(ClientsModel).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS') >= start_of_month
    ).all()

    df = pd.DataFrame([client.to_dict() for client in clients])
    output = BytesIO()

    if format == "xlsx":
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Daily New Clients")
        output.seek(0)
        headers = {
            'Content-Disposition': f'attachment; filename=daily_new_clients_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        }
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif format == "csv":
        df.to_csv(output, index=False)
        output.seek(0)
        headers = {
            'Content-Disposition': f'attachment; filename=daily_new_clients_{datetime.now().strftime("%Y-%m-%d")}.csv'
        }
        media_type = 'text/csv'
    else:
        raise HTTPException(status_code=400, detail="Invalid format specified.")

    # Return the in-memory file as a response
    return Response(content=output.getvalue(), media_type=media_type, headers=headers)


@report_router.get('/daily-client-hourly-count', summary="Get Hourly Counts for Daily New Clients")
async def get_daily_client_hourly_count():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # Query to extract hour and count clients
    hourly_data = session.query(
        func.extract('hour', func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS')).label('hour'),
        func.count(ClientsModel.id).label('count')
    ).filter(
        func.to_timestamp(ClientsModel.first_seen, 'YYYY-MM-DD HH24:MI:SS').between(today_start, today_end)
    ).group_by('hour').all()

    hourly_counts = {hour: 0 for hour in range(24)}

    for record in hourly_data:
        hour = int(record.hour)
        hourly_counts[hour] = record.count

    result = [{'hour': hour, 'count': count} for hour, count in hourly_counts.items()]
    return result
