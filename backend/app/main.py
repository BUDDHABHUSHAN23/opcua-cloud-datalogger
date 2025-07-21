from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware  #  this are the Frontend 
from app.api.routes import servers, groups, tags, reports, monitoring , ws, control , browse  # Import your routers
from app.db.database import engine, Base
import logging
logging.getLogger("asyncua").setLevel(logging.WARNING)

# Initialize FastAPI app
app = FastAPI(title="OPC UA Cloud Datalogger")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(servers.router, prefix="/api/servers", tags=["Servers"])
app.include_router(groups.router, prefix="/api/groups", tags=["Groups"])
app.include_router(tags.router, prefix="/api/tags", tags=["Tags"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(monitoring.router, prefix="/api/monitor", tags=["Monitor"])
app.include_router(ws.router, prefix="/api/ws", tags=["WebSocket"])
app.include_router(control.router, prefix="/api/control", tags=["Control"])
app.include_router(browse.router, prefix="/api/browse", tags=["Browse"])



# Auto-create tables at startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to OPC UA Cloud Datalogger API"}
