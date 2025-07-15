from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import servers, groups, tags, reports, monitoring
from app.db.database import engine, Base

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

# Auto-create tables at startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to OPC UA Cloud Datalogger API"}
