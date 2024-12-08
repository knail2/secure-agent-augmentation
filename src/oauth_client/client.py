import requests
import os

# This client adjusts based on ENVIRONMENT:
# If ENVIRONMENT=local, we assume API_BASE_URL="http://localhost:8000"
# If ENVIRONMENT=heroku, we might use a different URL
# If ENVIRONMENT=snowflake, another URL
ENV = os.getenv("ENVIRONMENT", "local").lower()

if ENV == "local":
    API_BASE_URL = "http://localhost:8000"
    ADMIN_API_URL = "http://localhost:9000"
elif ENV == "heroku":
    # On Heroku, set these URLs accordingly
    API_BASE_URL = "https://my-heroku-app.herokuapp.com"
    ADMIN_API_URL = "https://my-heroku-admin-app.herokuapp.com"
elif ENV == "snowflake":
    # On Snowflake environment
    API_BASE_URL = "https://my-snowflake-container-env.com"
    ADMIN_API_URL = "https://my-snowflake-admin-app.com"
else:
    API_BASE_URL = "http://localhost:8000"
    ADMIN_API_URL = "http://localhost:9000"

def main():
    print(f"Running in {ENV} environment:")
    print("Fetching list of clients from admin API:")
    resp = requests.get(f"{ADMIN_API_URL}/clients")
    print("Clients:", resp.json())

    print("\nCreating a new client:")
    resp = requests.post(f"{ADMIN_API_URL}/clients", params={"scope":"protected"})
    client_data = resp.json()
    print("Created client:", client_data)

    client_id = client_data["client_id"]
    client_secret = client_data["client_secret"]

    print("\nRequesting token using client_credentials:")
    token_resp = requests.post(f"{API_BASE_URL}/token", data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "protected"
    })
    token_data = token_resp.json()
    print("Token response:", token_data)

    access_token = token_data.get("access_token")

    if access_token:
        print("\nCall public endpoint:")
        pub_resp = requests.get(f"{API_BASE_URL}/public")
        print("Public response:", pub_resp.json())

        print("\nCall protected endpoint with token:")
        prot_resp = requests.get(f"{API_BASE_URL}/protected", headers={"Authorization": f"Bearer {access_token}"})
        print("Protected response:", prot_resp.json())

        print("\nIntrospect the token:")
        introspect_resp = requests.post(f"{API_BASE_URL}/introspect", data={"token": access_token})
        print("Introspect response:", introspect_resp.json())

        print("\nRevoke the token:")
        revoke_resp = requests.post(f"{API_BASE_URL}/revoke", data={"token": access_token})
        print("Revoke response:", revoke_resp.json())

if __name__ == "__main__":
    main()