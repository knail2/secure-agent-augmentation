from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from src.api_server.database import SessionLocal
from src.api_server.models import OAuth2Client, ClientState
from src.api_server.utils import require_admin_auth
from uuid import uuid4

admin_gui_bp = Blueprint('admin_gui', __name__, url_prefix='/admin/gui')

@admin_gui_bp.route("/", methods=["GET"])
@require_admin_auth
def admin_gui():
    db = SessionLocal()
    try:
        clients = db.query(OAuth2Client).all()
        return render_template("admin_gui.html", clients=clients)
    finally:
        db.close()

@admin_gui_bp.route("/create_client", methods=["POST"])
@require_admin_auth
def admin_gui_create_client():
    scope = request.form.get("scope", "protected")
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
        return redirect(url_for("admin_gui.admin_gui"))
    finally:
        db.close()

@admin_gui_bp.route("/revoke_client", methods=["POST"])
@require_admin_auth
def admin_gui_revoke_client():
    client_id = request.form.get("client_id")
    db = SessionLocal()
    try:
        c = db.query(OAuth2Client).filter_by(client_id=client_id).first()
        if c:
            c.state = ClientState.revoked
            db.commit()
        return redirect(url_for("admin_gui.admin_gui"))
    finally:
        db.close()