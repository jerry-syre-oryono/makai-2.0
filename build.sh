#!/bin/bash

# build.sh
# Exit immediately if a command exits with a non-zero status.
set -e

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
python -m pip install -r requirements.txt

# Add the backend directory to PYTHONPATH so Django can find its modules
# This is crucial because manage.py is in a subdirectory
export PYTHONPATH=$PYTHONPATH:$(pwd)/makai_backend

echo "Running database migrations..."
python makai_backend/manage.py migrate

echo "Ensuring superuser exists..."
python makai_backend/manage.py ensure_admin

echo "Initializing Qdrant collections..."
python makai_backend/manage.py init_qdrant

echo "Collecting static files..."
python makai_backend/manage.py collectstatic --noinput

echo "Build script completed successfully."
