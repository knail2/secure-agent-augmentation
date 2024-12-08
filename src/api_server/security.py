import time, os, logging
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.jose import jwt, jwk
from sqlalchemy.orm import scoped_session
from sqlalchemy.future import select
from .config import TOKEN_EXPIRY_SECONDS, ENV, ISSUER_URL
from .database import SessionLocal
from .models import OAuth2Client, OAuth2Token, ClientState

logger = logging.getLogger(__name__)

# Load JWT keys based on environment
if ENV == "local":
    HOME = os.path.expanduser("~")
    with open(os.path.join(HOME, ".ssh/jwt_private_key.pem"), "r") as f:
        JWT_PRIVATE_KEY = f.read()
    with open(os.path.join(HOME, ".ssh/jwt_public_key.pem"), "r") as f:
        JWT_PUBLIC_KEY = f.read()
else:
    JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
    JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
    if not JWT_PRIVATE_KEY or not JWT_PUBLIC_KEY:
        raise RuntimeError("JWT keys not found in environment for non-local environment.")

class ClientCredentialsGrant(grants.ClientCredentialsGrant):
    def authenticate_client(self):
        return self.request.client

    def create_access_token(self, token, request):
        issued_at = int(time.time())
        scope = token.get("scope", "")
        headers = {"alg": "RS256"}
        payload = {
            "iss": ISSUER_URL,  # Use the environment-based issuer URL
            "aud": request.client.client_id,
            "exp": issued_at + TOKEN_EXPIRY_SECONDS,
            "iat": issued_at,
            "scope": scope
        }
        access_token_raw = jwt.encode(headers, payload, JWT_PRIVATE_KEY)
        access_token = access_token_raw.decode() if hasattr(access_token_raw, 'decode') else access_token_raw
        token["access_token"] = access_token
        token["token_type"] = "Bearer"
        token["expires_in"] = TOKEN_EXPIRY_SECONDS
        return token

def query_client(client_id):
    db = SessionLocal()
    try:
        client = db.query(OAuth2Client).filter_by(client_id=client_id).first()
        if client and client.state == ClientState.active:
            return client
        return None
    finally:
        db.close()

def save_token(token_data, request):
    db = SessionLocal()
    try:
        issued_at = int(time.time())
        access_token = token_data["access_token"]
        scope = token_data.get("scope", "")
        t = OAuth2Token(
            client_id=request.client.client_id,
            access_token=access_token,
            refresh_token=None,
            scope=scope,
            issued_at=issued_at,
            expires_in=TOKEN_EXPIRY_SECONDS
        )
        db.add(t)
        db.commit()
    finally:
        db.close()

def validate_jwt_token(token_str: str):
    try:
        claims = jwt.decode(token_str, JWT_PUBLIC_KEY)
        claims.validate()
        return claims
    except Exception as e:
        logger.info(f"Token validation failed: {e}")
        return None

authorization_server = AuthorizationServer(query_client=query_client, save_token=save_token)