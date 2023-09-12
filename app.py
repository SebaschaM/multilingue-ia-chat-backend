from flask import Flask
from src.routes.auth import auth_bp
from src.database.db_pg import db
from src.utils.send_mail import configure_mail
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(auth_bp)
    mail = configure_mail(app)
    return app
