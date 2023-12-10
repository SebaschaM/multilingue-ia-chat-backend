from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

import os

from src.database.db_pg import db
from src.utils.send_mail import configure_mail
from src.utils.schedules import Schedules
from src.utils.keywords_sql_inyection import sql_keywords, sql_booleans
from src.routes import blueprints


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
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


@app.before_request
def before_request():
    if request.method == "POST":
        request_form = request.get_json() if request.is_json else request.form

        for key, value in request_form.items():
            if isinstance(value, str):
                words = value.upper().split()
                if any(keyword in words for keyword in sql_keywords) or any(
                    boolean in words for boolean in sql_booleans
                ):
                    print("SQL INJECTION DETECTED")
                    print(value)
                    response = jsonify(
                        success=False,
                        message="Entrada no válida: se ha detectado un intento de inyección SQL",
                    )
                    response.status_code = 400
                    response.headers["Content-Type"] = "application/json"
                    return response

        return None


def create_app():
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    mail = configure_mail(app)
    scheduler_block_users = BackgroundScheduler(daemon=True)
    scheduler_block_users.add_job(
        Schedules.block_users, "interval", seconds=10, args=(app, db)
    )
    scheduler_block_users.start()

    scheduler_inactive_notification = BackgroundScheduler(daemon=True)
    scheduler_inactive_notification.add_job(
        Schedules.verification_notifications_change_to_desactive,
        "interval",
        seconds=10,
        args=(app, db),
    )
    scheduler_inactive_notification.start()

    return app
