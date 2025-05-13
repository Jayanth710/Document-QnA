import logging
import os

from flask import app
from DocuMind.app.app_server import create_app
from app.environment import Environment

env  = Environment.from_env()

logging.basicConfig(level=env.root_log_level)
logging.getLogger('starter').setLevel(level=env.starter_log_level)

if __name__ == "__main__":
    create_app(env).run(
        debug=os.environ.get("DEBUG", "true"),
        host="0.0.0.0",
        port=8080)
