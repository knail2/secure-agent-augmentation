from starlette.middleware.base import BaseHTTPMiddleware
import logging
from starlette.requests import Request
from fastapi import HTTPException, status
from .security import validate_jwt_token

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response

class TokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_endpoints = ["/public", "/token", "/introspect", "/revoke"]
        if any(request.url.path.startswith(ep) for ep in open_endpoints):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

        token_str = auth_header.split(" ", 1)[1]
        claims = await validate_jwt_token(token_str)
        if not claims:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

        request.state.token_claims = claims
        return await call_next(request)