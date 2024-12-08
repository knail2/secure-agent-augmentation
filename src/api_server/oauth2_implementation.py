from flask import Blueprint, request, jsonify
from sqlalchemy.orm import scoped_session
from sqlalchemy.future import select
from authlib.jose import jwk
from .security import authorization_server, validate_jwt_token, JWT_PUBLIC_KEY
from .database import SessionLocal
from .models import OAuth2Token

bp = Blueprint('oauth2', __name__)

@bp.route("/token", methods=["POST"])
def token_endpoint():
    # grant_type=client_credentials expected
    return authorization_server.create_token_response(request)

@bp.route("/introspect", methods=["POST"])
def introspect():
    token = request.form.get("token")
    claims = validate_jwt_token(token)
    if claims:
        return jsonify({"active": True, "scope": claims.get("scope", "")})
    else:
        return jsonify({"active": False})

@bp.route("/revoke", methods=["POST"])
def revoke():
    token = request.form.get("token")
    db = SessionLocal()
    try:
        t = db.query(OAuth2Token).filter_by(access_token=token).first()
        if t:
            db.delete(t)
            db.commit()
    finally:
        db.close()
    return jsonify({"status": "ok"})

@bp.route("/jwks", methods=["GET"])
def jwks_endpoint():
    public_jwk = jwk.dumps(JWT_PUBLIC_KEY, kty='RSA')
    return jsonify({"keys": [public_jwk]})