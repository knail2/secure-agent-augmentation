from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from ....database import SessionLocal
from ....models import OAuth2Client, ClientState
from ....utils import require_admin_auth
from uuid import uuid4

admin_api_bp = Blueprint('admin_api', __name__, url_prefix='/admin/api')

@admin_api_bp.route("/clients", methods=["GET"])
@require_admin_auth
def list_clients_api():
    db = SessionLocal()
    try:
        clients = db.query(OAuth2Client).all()
        result = []
        for c in clients:
            masked_secret = "****" + c.client_secret[-4:] if c.client_secret else None
            result.append({
                "client_id": c.client_id,
                "client_secret": masked_secret,
                "scope": c.scope,
                "state": c.state.value
            })
        return jsonify(result)
    finally:
        db.close()

@admin_api_bp.route("/clients", methods=["POST"])
@require_admin_auth
def create_client_api():
    scope = request.args.get("scope", "protected")
    db = SessionLocal()
    try:
        client_id = uuid4().hex
        client_secret = uuid4().hex
        client = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="",
            scope=scope,
            grant_types="client_credentials",
            response_types="",
            token_endpoint_auth_method="client_secret_basic",
            state=ClientState.active
        )
        db.add(client)
        db.commit()
        return jsonify({
            "client_id": client_id,
            "client_secret": client_secret
        })
    finally:
        db.close()

@admin_api_bp.route("/clients/revoke", methods=["POST"])
@require_admin_auth
def revoke_client_api():
    client_id = request.args.get("client_id")
    db = SessionLocal()
    try:
        c = db.query(OAuth2Client).filter_by(client_id=client_id).first()
        if not c:
            return jsonify({"error": "Client not found"}), 404
        c.state = ClientState.revoked
        db.commit()
        return jsonify({"status": "revoked"})
    finally:
        db.close()