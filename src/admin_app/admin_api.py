from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from ..api_server.database import SessionLocal
from ..api_server.models import OAuth2Client, ClientState
import uuid

admin_api = FastAPI(title="Admin API")

@admin_api.get("/clients")
async def list_clients():
    async with SessionLocal() as db:
        q = await db.execute(select(OAuth2Client))
        clients = q.scalars().all()
        return [
            {
                "client_id": c.client_id,
                "client_secret": "****" + c.client_secret[-4:],
                "scope": c.scope,
                "state": c.state.value
            }
            for c in clients
        ]

@admin_api.post("/clients")
async def create_client(scope: str):
    client_id = uuid.uuid4().hex
    client_secret = uuid.uuid4().hex
    client = OAuth2Client(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="",
        scope=scope,
        grant_types="client_credentials",
        response_types="",
        token_endpoint_auth_method="client_secret_basic",
        state=ClientState.active
    )
    async with SessionLocal() as db:
        db.add(client)
        await db.commit()
    return {
        "client_id": client_id,
        "client_secret": client_secret
    }

@admin_api.post("/clients/revoke")
async def revoke_client(client_id: str):
    async with SessionLocal() as db:
        q = await db.execute(select(OAuth2Client).where(OAuth2Client.client_id == client_id))
        c = q.scalar_one_or_none()
        if not c:
            raise HTTPException(status_code=404, detail="Client not found")
        c.state = ClientState.revoked
        await db.commit()
    return {"status": "revoked"}