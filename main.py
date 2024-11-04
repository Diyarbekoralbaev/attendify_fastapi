from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import employee_router, attendance_router, client_router, department_router, report_router, working_graphic_router, image_handle_router
from init_db import init_db
from manager import manager

app = FastAPI(
    title="AralVision API",
    description="This is the API for AralVision. It provides endpoints for managing employees, attendance, clients, and departments.",
    version="0.1.0",
)

# Configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,               # Specifies the allowed origins
    allow_credentials=True,              # Allows cookies and authentication headers
    allow_methods=["*"],                 # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                 # Allows all headers
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="media")

# Include routers
app.include_router(employee_router, prefix="/employee")
app.include_router(attendance_router, prefix="/attendance")
app.include_router(client_router, prefix="/client")
app.include_router(department_router, prefix="/department")
app.include_router(report_router, prefix="/report")
app.include_router(working_graphic_router, prefix="/working-graphic")
app.include_router(image_handle_router, prefix="/image")

# Initialize the database on startup
@app.on_event('startup')
async def on_startup():
    init_db()
    print('DB initialized')

# Root endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
