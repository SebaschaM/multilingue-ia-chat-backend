from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import logging
import os

# Import socket io
from flask_socketio import SocketIO


# Routes Admin
from src.routes.admin.auth_admin import auth_admin_bp


# Routes client
from src.routes.client.auth_client import auth_client_bp

from src.database.db_pg import db
from src.utils.send_mail import configure_mail

# Import models
from src.models.roles import Roles
from src.models.conversations import Conversations
from src.models.sessions import Sessions
from src.models.messages import Messages
from src.models.users import Users
from src.models.clients import Clients

load_dotenv()
cors_allowed_origins = "*"

socketio = SocketIO(cors_allowed_origins=cors_allowed_origins)


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(auth_admin_bp)
    app.register_blueprint(auth_client_bp)
    # app.register_blueprint(message_bp)
    mail = configure_mail(app)
    return app


# !Esto no deberia estar aqui
if __name__ == "__main__":
    # Inicializa SocketIO solo si el archivo se ejecuta directamente
    socketio.run(create_app(), debug=True)
from src.sockets.socketios_event import (
    handle_connect,
    handle_login,
    handle_create_private_room,
    handle_join_private_room,
)
