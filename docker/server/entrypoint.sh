#! /bin/bash

gunicorn --log-level INFO --timeout 120 --reload --bind 0.0.0.0:5000 -w 4 mushroom.server_app:flask_app
