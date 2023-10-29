from flask import Flask, request, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

from src.database.db_pg import db
from src.utils.send_mail import configure_mail
from src.utils.schedules import Schedules
from src.routes import blueprints
from src.sockets.user.socketio_events import (
    handle_assign_user_to_room,
    handle_send_message,
    handle_close_room,
)

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
# socketio.init_app(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["15 per minute"],
    storage_uri="memory://",
    strategy="fixed-window",
)


@app.errorhandler(429)
def ratelimit_handler(e):
    return (
        jsonify(
            success=False,
            message=f"Has superado el límite de solicitudes, vuelve a intentarlo en un minuto",
        ),
        429,
    )


def create_app():
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    mail = configure_mail(app)
    programador = BackgroundScheduler(daemon=True)
    programador.add_job(Schedules.block_users, "interval", seconds=10, args=(app, db))
    programador.start()

    return app
