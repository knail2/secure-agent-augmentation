from flask import Blueprint, request, jsonify
from pydantic import BaseModel

auth_testing_bp = Blueprint('auth_testing', __name__)

class HaikuData(BaseModel):
    line1: str
    line2: str
    line3: str

@auth_testing_bp.route("/public", methods=["GET"])
def public_endpoint():
    return jsonify({"message": "This is public and requires no auth"})

@auth_testing_bp.route("/protected", methods=["GET"])
def protected_endpoint():
    claims = getattr(request, 'token_claims', {})
    scopes = claims.get("scope", "")
    if "protected" in scopes or "highly_sensitive" in scopes:
        return jsonify({"message": "This is protected and authorized"})
    else:
        return jsonify({"error": "Forbidden"}), 403

@auth_testing_bp.route("/protected_post", methods=["POST"])
def protected_post_endpoint():
    claims = getattr(request, 'token_claims', {})
    scopes = claims.get("scope", "")
    if "protected" in scopes or "highly_sensitive" in scopes:
        data = request.get_json()
        haiku = f"{data['line1']}\n{data['line2']}\n{data['line3']}\n(Authorized Request)"
        return jsonify({"haiku": haiku})
    else:
        return jsonify({"error": "Forbidden"}), 403

@auth_testing_bp.route("/highly_confidential", methods=["GET"])
def highly_confidential_endpoint():
    claims = getattr(request, 'token_claims', {})
    scopes = claims.get("scope", "")
    if "highly_sensitive" in scopes:
        return jsonify({"message": "This is highly confidential"})
    else:
        return jsonify({"error": "Forbidden"}), 403