import csv
import json
import time
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Form
from authlib.integrations.starlette_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.jose import jwt
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from authlib.oidc.core import OpenIDCode
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Store clients, tokens, etc in CSV for now
CLIENTS_CSV = 'clients.csv'
TOKENS_CSV = 'tokens.csv'
SECRET_KEY = os.getenv('SECRET_KEY')

app = FastAPI()
authorization = AuthorizationServer()

# Helper functions to read/write CSV
def read_clients():
    with open(CLIENTS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_token(token_data):
    with open(TOKENS_CSV, mode='a') as file:
        writer = csv.DictWriter(file, fieldnames=token_data.keys())
        writer.writerow(token_data)

# Grant classes
class AuthorizationCodeGrant(OpenIDCode):
    def authenticate_user(self, client, code):
        # Add authentication logic
        return {"user_id": "example_user_id"}

    def create_access_token(self, client, grant_user, scope):
        header = {"alg": "HS256"}
        payload = {
            "sub": grant_user['user_id'],
            "scope": scope,
            "exp": int(time.time()) + 3600
        }
        return jwt.encode(header, payload, SECRET_KEY)

@app.post('/authorize')
async def authorize(
    request: Request,
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    scope: str = Form(...),
    response_type: str = Form(...),
    state: str = Form(...),
):
    clients = read_clients()
    client = next((c for c in clients if c['client_id'] == client_id), None)
    if not client:
        raise HTTPException(status_code=400, detail='Invalid client_id')

    # Fake user authentication (you would want a real authentication here)
    user = {"user_id": "user1"}

    grant = AuthorizationCodeGrant()  # Grant type
    code = grant.create_authorization_code(request, client, user, scope)
    # Store in token store
    token_data = {
        'client_id': client_id,
        'user_id': user['user_id'],
        'scope': scope,
        'code': code,
        'redirect_uri': redirect_uri
    }
    write_token(token_data)

    # Redirect to client's callback URL
    url = f"{redirect_uri}?code={code}&state={state}"
    return RedirectResponse(url)

# Token endpoint
@app.post('/token')
async def issue_token(
    client_id: str = Form(...),
    client_secret: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    grant_type: str = Form(...),
):
    clients = read_clients()
    client = next((c for c in clients if c['client_id'] == client_id), None)
    if not client or client['client_secret'] != client_secret:
        raise HTTPException(status_code=400, detail='Invalid client credentials')

    with open(TOKENS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        token_data = next((r for r in reader if r['code'] == code), None)
    if not token_data:
        raise HTTPException(status_code=400, detail='Invalid code')

    # Generate access token
    header = {"alg": "HS256"}
    payload = {
        "sub": token_data['user_id'],
        "scope": token_data['scope'],
        "exp": int(time.time()) + 3600
    }
    access_token = jwt.encode(header, payload, SECRET_KEY)
    id_token = jwt.encode(header, {"sub": token_data['user_id'], "iat": int(time.time())}, SECRET_KEY)

    response = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600,
        "id_token": id_token
    }
    return JSONResponse(response)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
