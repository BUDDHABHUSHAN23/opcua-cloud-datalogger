from httpx import ASGITransport
from app.main import app

# Shared transport instance using FastAPI app (for test clients)
transport = ASGITransport(app=app)
