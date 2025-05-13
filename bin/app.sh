#!/usr/bin/env bash

# Ensure PORT is set (defaults to 8080 if missing)
PORT=${PORT:-8080}

if [ -f /apps/.env ]; then
    export $(grep -v '^#' /apps/.env | xargs)
fi

echo "Starting Gunicorn on port $PORT..."
exec gunicorn -w 4 'app.app_server:create_app()' --bind=0.0.0.0:$PORT --timeout 120
# exec gunicorn 'app.app_server:create_app()' \
#     --workers 4 \
#     --bind 0.0.0.0:$PORT \
#     --timeout 120