#!/bin/bash
pip install -r requirements.txt
python makai_backend/manage.py collectstatic --noinput
python makai_backend/manage.py migrate
