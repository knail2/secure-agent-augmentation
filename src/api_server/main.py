import logging
from fastapi import FastAPI
from talisman import Talisman
from .config import ENV
from .database import Base, engine
from .security import init_auth_server
from .middleware import LoggingMiddleware, TokenValidationMiddleware
from .oauth2_implementation import router as oauth2_router
from .routers.auth_testing import endpoints as auth_testing_endpoints
#from .routers.release_oversight import endpoints as release_oversight_endpoints
#from .routers.service_ticket_analysis import endpoints as service_ticket_analysis_endpoints
#from .routers.tableau_dashboard_usage import endpoints as tableau_dashboard_usage_endpoints
#from .routers.internal_audit_analysis import endpoints as internal_audit_analysis_endpoints
#from .routers.slack_analysis import endpoints as slack_analysis_endpoints
#from .routers.common_actions import endpoints as common_actions_endpoints

logger = logging.getLogger(__name__)

app = FastAPI(title="OAuth2 Server (Client Credentials)")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

init_auth_server(app)

app.add_middleware(LoggingMiddleware)
app.add_middleware(TokenValidationMiddleware)

if ENV != "local":
    Talisman(app, force_https=True)
else:
    Talisman(app, force_https=False)

app.include_router(oauth2_router)
app.include_router(auth_testing_endpoints.router)
# app.include_router(release_oversight_endpoints.router)
# app.include_router(service_ticket_analysis_endpoints.router)
# app.include_router(tableau_dashboard_usage_endpoints.router)
# app.include_router(internal_audit_analysis_endpoints.router)
# app.include_router(slack_analysis_endpoints.router)
# app.include_router(common_actions_endpoints.router)