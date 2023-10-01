# Database
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

from src.database.db_pg import db
from src.models.clients import Clients
from src.utils.security import Security
from src.utils.send_mail import send_email, configure_mail


class AuthClientService:
    @classmethod
    def verify_email_exists(cls, email):
        try:
            client = Clients.query.filter_by(email=email).first()

            if not client:
                return {
                    "error": "El cliente no existe",
                    "client_exists": False,
                    "success": True,
                }, 200

            return {
                "message": "El cliente existe",
                "client_exists": True,
                "success": True,
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def register_user_no_full(cls, user_data):
        try:
            clientExists = cls.verify_email_exists(user_data["email"])
            if clientExists[0]["client_exists"]:
                return {
                    "error": "El cliente ya existe",
                    "client_exists": True,
                    "success": False,
                }, 400

            token_email = str(uuid.uuid4())
            new_client = Clients(
                email=user_data["email"],
                fullname=user_data["fullname"],
                cellphone=user_data["cellphone"],
                language_id=user_data["language_id"],
                created_at=datetime.now(),
            )
            db.session.add(new_client)
            db.session.commit()

            return {
                "message": "Cliente registrado en la base de datos",
                "client_exists": False,
                "success": True,
            }, 201

        except Exception as e:
            print(e)
            return {
                "error": str(e),
                "success": False,
            }, 500
