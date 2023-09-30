from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import logging
import os

from src.database.db_pg import db
from src.utils.send_mail import configure_mail

# Import socket io
from flask_socketio import SocketIO
from src.routes import blueprints

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

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

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
