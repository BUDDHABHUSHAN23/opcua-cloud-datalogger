# Async OPC UA reads
from asyncua import Client as UaClient
from app.db.crud import server as server_crud
from app.db.database import SessionLocal

opc_clients = {}

async def get_opc_client(server_id: int):
    db = SessionLocal()
    server = server_crud.get_all_servers(db)
    db.close()
    endpoint = None
    for s in server:
        if s.id == server_id:
            endpoint = s.endpoint_url
            break
    if not endpoint:
        return None
    if endpoint in opc_clients:
        return opc_clients[endpoint]
    client = UaClient(endpoint)
    try:
        await client.connect()
        opc_clients[endpoint] = client
        return client
    except Exception:
        return None