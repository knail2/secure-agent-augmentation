import streamlit as st
import requests
import os

# ADMIN_API_URL can be set depending on ENV. For simplicity, assume it comes from env or defaults to local.
ADMIN_API_URL = os.getenv("ADMIN_API_URL", "http://localhost:9000")

st.title("Admin Client Management (Machine-to-Machine)")

scope = st.text_input("Scope", "protected")

if st.button("Create Client"):
    resp = requests.post(f"{ADMIN_API_URL}/clients", params={"scope": scope})
    if resp.status_code == 200:
        data = resp.json()
        st.write("Client Created:")
        st.write(data)
    else:
        st.write("Error creating client:", resp.text)

st.write("### List Clients")
resp = requests.get(f"{ADMIN_API_URL}/clients")
if resp.status_code == 200:
    clients = resp.json()
    st.table(clients)
else:
    st.write("Error listing clients:", resp.text)

st.write("### Revoke Client")
client_to_revoke = st.text_input("Client ID to Revoke")
if st.button("Revoke"):
    resp = requests.post(f"{ADMIN_API_URL}/clients/revoke", params={"client_id": client_to_revoke})
    if resp.status_code == 200:
        st.write("Client revoked")
    else:
        st.write("Error revoking:", resp.text)