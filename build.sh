#!/bin/bash

# build.sh
# Exit immediately if a command exits with a non-zero status.
set -e

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
python -m pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate

echo "Ensuring superuser exists..."
python manage.py ensure_admin

echo "Initializing Qdrant collections..."
python manage.py init_qdrant

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build script completed successfully."
