import logging
from flask import Flask, request
from talisman import Talisman
from .config import ENV
from .database import Base, engine
from .security import authorization_server, validate_jwt_token
from .oauth2_implementation import bp as oauth2_bp
from .routers.auth_testing.endpoints import auth_testing_bp
# Import other endpoint blueprints as needed...
from .admin.api.endpoints import admin_api_bp
from .admin.gui.endpoints import admin_gui_bp

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    with engine.connect() as conn:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    authorization_server.init_app(app)

    if ENV != "local":
        Talisman(app, force_https=True)
    else:
        Talisman(app, force_https=False)

    @app.before_request
    def log_request():
        logger.info(f"Request {request.method} {request.path}")

    @app.before_request
    def token_validation():
        # Allow public endpoints, token endpoints, jwks, introspect, revoke, and all admin routes
        # to skip token validation. Admin routes have their own basic auth.
        open_endpoints = ["/public", "/token", "/introspect", "/revoke", "/jwks", "/admin"]
        if any(request.path.startswith(ep) for ep in open_endpoints):
            return
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return ("Missing or invalid token", 401)
        token_str = auth_header.split(" ", 1)[1]
        claims = validate_jwt_token(token_str)
        if not claims:
            return ("Invalid or expired token", 401)
        setattr(request, 'token_claims', claims)

    @app.after_request
    def log_response(response):
        logger.info(f"Response status: {response.status_code}")
        return response

    # Register blueprints
    app.register_blueprint(oauth2_bp)
    app.register_blueprint(auth_testing_bp)
    # register other resource blueprints...
    app.register_blueprint(admin_api_bp)
    app.register_blueprint(admin_gui_bp)

    return app

app = create_app()