from pydantic import BaseModel
from typing import Optional

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: Optional[str]

class IntrospectResponse(BaseModel):
    active: bool
    scope: Optional[str]