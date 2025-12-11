#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! pg_isready -h db -U cinema_user -d online_cinema; do
  sleep 1
done

echo "Running database migrations..."
# Check if migrations directory exists and has migrations
if [ -d "alembic/versions" ] && [ "$(ls -A alembic/versions 2>/dev/null)" ]; then
    alembic upgrade head
else
    echo "No migrations found. Please create initial migration first."
    echo "Run: alembic revision --autogenerate -m 'Initial migration'"
fi

echo "Starting application..."
exec "$@"

