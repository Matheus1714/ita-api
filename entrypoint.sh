#!/bin/sh
set -e

echo "Running migrations..."
python -m alembic -c alembic.ini upgrade head

echo "Starting API..."
exec python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
