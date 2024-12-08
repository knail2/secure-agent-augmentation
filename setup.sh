#!/bin/bash

# Load variables from the .env file
set -a # Automatically export variables
source .env
set +a

# Check if required variables are set
if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_HOST" ]; then
  echo "Missing required environment variables in .env"
  exit 1
fi

# Use POSTGRES_DB for DB_NAME
DB_NAME=$POSTGRES_DB
DB_USER=$POSTGRES_USER
DB_PASSWORD=$POSTGRES_PASSWORD

# Export PostgreSQL connection variables
export PGUSER=$POSTGRES_USER
export PGPASSWORD=$POSTGRES_PASSWORD
export PGDATABASE=$POSTGRES_DB
export PGHOST=$POSTGRES_HOST
export PGPORT=${POSTGRES_PORT:-5432} # Default to 5432 if POSTGRES_PORT is not set

# Create a temporary SQL file with the variables replaced
TEMP_SQL_FILE=$(mktemp)
sed -e "s/\${DB_NAME}/$DB_NAME/g" \
    -e "s/\${DB_USER}/$DB_USER/g" \
    -e "s/\${DB_PASSWORD}/$DB_PASSWORD/g" \
    init/init_db.sql > "$TEMP_SQL_FILE"

# Execute the SQL script
psql -f "$TEMP_SQL_FILE"

# Check for errors
if [ $? -ne 0 ]; then
  echo "Database setup failed"
  rm -f "$TEMP_SQL_FILE"
  exit 1
else
  echo "Database setup completed successfully"
fi

# Clean up the temporary file
rm -f "$TEMP_SQL_FILE"