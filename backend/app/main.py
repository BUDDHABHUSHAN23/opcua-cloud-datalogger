from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware  #  this are the Frontend 
from app.api.routes import servers, groups, tags, reports, monitoring , ws, control , browse, control , auth , live # Import your routers
from app.db.database import engine, Base   # Import database engine and Base for ORM
#=======================================================#
import asyncio
from app.websocket.live_updates import live_data_publisher
#========================================================#

# from app.db.models import user      => # Import your database models if needed

import logging

Base.metadata.create_all(bind=engine)  # Create all tables in the database and initialize the database if not already done

# it helps to debug the application by showing the logs
logging.getLogger("asyncua").setLevel(logging.WARNING)   # Set asyncua logging level to WARNING keeps the logs clean

# Initialize FastAPI app
app = FastAPI(title="OPC UA Cloud Datalogger")   # this is for the redirect slashes HTTP to HTTPS


# CORS for frontend access
app.add_middleware(  
    CORSMiddleware,
    allow_origins=["*"],                                 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],                       # allow all origins, methods, and headers & this are the rules for CORS
)

# Register routes
app.include_router(servers.router, prefix="/api/servers", tags=["Servers"])         # servers router
app.include_router(groups.router, prefix="/api/groups", tags=["Groups"])
app.include_router(tags.router, prefix="/api/tags", tags=["Tags"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(monitoring.router, prefix="/api/monitor", tags=["Monitor"])
app.include_router(ws.router, prefix="/api/ws", tags=["WebSocket"])                  
app.include_router(control.router, prefix="/api/control", tags=["Control"])
app.include_router(browse.router, prefix="/api/browse", tags=["Browse"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(live.router, prefix="/api", tags=["LiveWebSocket"])

#############################################################################
@app.on_event("startup")
async def start_live_updates():
    asyncio.create_task(live_data_publisher())
##############################################################################

@app.get("/")       # Root endpoint for the API to health check
def root():
    return {"message": "Welcome to OPC UA Cloud Datalogger API"}
