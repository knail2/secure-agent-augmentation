# client.py
import requests
import webbrowser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')

# Step 1: Authorization
params = {
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'response_type': 'code',
    'scope': 'openid profile',
    'state': 'xyz'
}
url = f"{AUTH_URL}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type=code&scope={params['scope']}&state={params['state']}"
webbrowser.open(url)

# Assuming the callback redirects back to REDIRECT_URI with code in params
code = input("Enter the code from the callback URL: ")

# Step 2: Token
token_data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': code,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code'
}
response = requests.post(TOKEN_URL, data=token_data)
print(response.json())
