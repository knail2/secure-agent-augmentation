import enum
import uuid
from sqlalchemy import Column, String, Text, Integer, Enum
from .database import Base

class ClientState(enum.Enum):
    active = "active"
    revoked = "revoked"

class OAuth2Client(Base):
    __tablename__ = 'oauth2_client'
    client_id = Column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    client_secret = Column(String(128))
    redirect_uri = Column(Text)
    scope = Column(Text)
    grant_types = Column(Text)       # "client_credentials"
    response_types = Column(Text)    # could be empty
    token_endpoint_auth_method = Column(Text)
    state = Column(Enum(ClientState), default=ClientState.active)

class OAuth2Token(Base):
    __tablename__ = 'oauth2_token'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(64))
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    scope = Column(Text)
    issued_at = Column(Integer)
    expires_in = Column(Integer)