#!/bin/bash

# build.sh

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
# Adjusting path to manage.py since it is inside makai_backend/
python makai_backend/manage.py migrate

echo "Ensuring superuser exists..."
python makai_backend/manage.py ensure_admin

echo "Initializing Qdrant collections..."
python makai_backend/manage.py init_qdrant

echo "Collecting static files..."
python makai_backend/manage.py collectstatic --noinput
