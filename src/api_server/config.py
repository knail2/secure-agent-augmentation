import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENVIRONMENT", "local").lower()
TOKEN_EXPIRY_SECONDS = int(os.getenv("TOKEN_EXPIRY_SECONDS", 3600))
ISSUER_URL = os.getenv("ISSUER_URL", "http://localhost:8000")

if ENV == "local":
    POSTGRES_USER = os.getenv("POSTGRES_USER", "local_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "local_password")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "local_db")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

elif ENV == "heroku":
    heroku_db_url = os.getenv("DATABASE_URL")
    if heroku_db_url.startswith("postgres://"):
        heroku_db_url = heroku_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = heroku_db_url

elif ENV == "snowflake":
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
    if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA]):
        raise ValueError("Missing Snowflake credentials.")
    DATABASE_URL = f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"

else:
    raise ValueError("Unknown ENVIRONMENT setting.")