from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

@router.get("/public")
async def public_endpoint():
    return {"message": "This is public and requires no auth"}

@router.get("/protected")
async def protected_endpoint(request: Request):
    claims = getattr(request.state, 'token_claims', {})
    scopes = claims.get("scope", "")
    if "protected" in scopes or "highly_sensitive" in scopes:
        return {"message": "This is protected and authorized"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

class HaikuData(BaseModel):
    line1: str
    line2: str
    line3: str

@router.post("/protected_post")
async def protected_post_endpoint(request: Request, data: HaikuData):
    claims = getattr(request.state, 'token_claims', {})
    scopes = claims.get("scope", "")
    if "protected" in scopes or "highly_sensitive" in scopes:
        return {"haiku": f"{data.line1}\n{data.line2}\n{data.line3}\n(Authorized Request)"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/highly_confidential")
async def highly_confidential_endpoint(request: Request):
    claims = getattr(request.state, 'token_claims', {})
    scopes = claims.get("scope", "")
    if "highly_sensitive" in scopes:
        return {"message": "This is highly confidential"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)