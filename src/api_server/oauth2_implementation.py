from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from authlib.jose import jwk
from .security import authorization_server, validate_jwt_token, JWT_PUBLIC_KEY
from .database import SessionLocal
from .models import OAuth2Token

router = APIRouter()

@router.post("/token")
async def token_endpoint(request: Request):
    # grant_type=client_credentials expected
    return await authorization_server.create_token_response(request)

@router.post("/introspect")
async def introspect(token: str = Form(...)):
    claims = await validate_jwt_token(token)
    if claims:
        return {"active": True, "scope": claims.get("scope", "")}
    else:
        return {"active": False}

@router.post("/revoke")
async def revoke_token(token: str = Form(...)):
    async with SessionLocal() as db:
        q = await db.execute(select(OAuth2Token).where(OAuth2Token.access_token == token))
        t = q.scalar_one_or_none()
        if t:
            await db.delete(t)
            await db.commit()
    return {"status": "ok"}

@router.get("/jwks")
async def jwks_endpoint():
    # Convert the public key from PEM to JWK format
    # Authlib jwk.dumps can take a public_key in PEM format and produce JWK
    public_jwk = jwk.dumps(JWT_PUBLIC_KEY, kty='RSA')
    # Return the JWKS
    return JSONResponse(content={"keys": [public_jwk]})