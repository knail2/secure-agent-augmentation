-- Check if the user exists, and if not, create it with the specified password
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = '${DB_USER}'
    ) THEN
        CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
    END IF;
END $$;

-- Check if the database exists, and if not, create it
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_database
        WHERE datname = '${DB_NAME}'
    ) THEN
        CREATE DATABASE ${DB_NAME};
    END IF;
END $$;

-- Assign the database ownership to the user
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = '${DB_USER}'
    ) THEN
        ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};
    END IF;
END $$;

-- Grant all privileges on the database to the user
DO $$