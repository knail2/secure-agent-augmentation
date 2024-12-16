#!/bin/bash
# Install Homebrew if not installed
if ! command -v brew &> /dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install PostgreSQL
echo "Installing PostgreSQL..."
brew install postgresql

# Start PostgreSQL
echo "Starting PostgreSQL..."
brew services start postgresql

# Verify Installation
echo "PostgreSQL installed successfully. Version:"
psql --version
