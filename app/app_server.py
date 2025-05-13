import logging
import os
from flask import Flask
import sqlalchemy
from sqlalchemy.sql import text
from app.helper_functions import chatqna, loader, splitter, embedding, weaviate_client, qa_pipeline
from app.database_support.database_template import DatabaseTemplate
from app.environment import Environment
from app.chat_api import chat_api
from app.index_page import index_page
from app.upload_api import upload_api
from app.qna_api import qna_api
from app.auth import auth_api
from flask_cors import CORS

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
    )

logger = logging.getLogger(__name__)

def create_app(env: Environment = Environment.from_env()) -> Flask:
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    logger.info("Database connection")
    app.secret_key = "a9b8c7d6e5f4g3h2i1j0"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_CONNECTION_STRING", "CONN_STR_NOT_FOUND")
    
    app.config.update(
        SESSION_COOKIE_SAMESITE="None",
        SESSION_COOKIE_SECURE=True,
    )
    
    db = sqlalchemy.create_engine(
       os.environ.get("DB_CONNECTION_STRING", "CONN_STR_NOT_FOUND"),
       pool_size=5,
    )

    # Test database connection with proper SQL construct
    try:
        with db.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

    db_template = DatabaseTemplate(db)

    logger.info("Database connection initialized")

    try:
        app.register_blueprint(index_page())
        app.register_blueprint(auth_api(db_template))
        app.register_blueprint(chat_api(db_template))
        app.register_blueprint(upload_api(db_template))
        app.register_blueprint(qna_api(db_template))
        logger.info("Blueprints registered successfully")
    except Exception as e:
        logger.error(f"Failed to register blueprints: {e}")
        raise

    return app

if __name__ == "__main__":
    logger.info("Starting")
    app = create_app()
    try:
        logger.info("Starting Flask app on http://0.0.0.0:8080")
        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Flask app failed to start: {e}")
        raise