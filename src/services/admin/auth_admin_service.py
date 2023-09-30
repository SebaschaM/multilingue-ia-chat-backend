# Database
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

from src.database.db_pg import db
from src.models.users import Users
from src.utils.security import Security
from src.utils.send_mail import send_email, configure_mail


class AuthAdminService:
    @classmethod
    def verify_email_exists(cls, email):
        try:
            user = Users.query.filter_by(email=email).first()

            if not user:
                return {
                    "error": "El usuario no existe.",
                    "success": False,
                }, 400

            return {
                "message": "El usuario existe.",
                "success": True,
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def login_user(cls, email, password):
        try:
            user = Users.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return {
                    "error": "Correo electrónico o contraseña incorrectos.",
                    "success": False,
                }, 401

            if user.user_verified == 0:
                return {
                    "error": "El usuario no ha sido verificado.",
                    "success": False,
                }, 401

            encoded_token = Security.generate_token(user)
            return {
                "message": "Inicio de sesión exitoso.",
                "user": user.to_dict(),
                "success": True,
                "jwt_token": encoded_token,
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def register_user(cls, user_data):
        try:
            print("almenos")
            email = user_data["email"]
            password = generate_password_hash(user_data["password"])
            fullname = user_data["fullname"]
            cellphone = user_data["cellphone"]
            language_id = user_data["language_id"]
            role_id = user_data["role_id"]

            user = Users.query.filter_by(email=email).first()

            if user:
                return {
                    "error": "El usuario ya existe",
                    "success": False,
                }, 400

            token_email = str(uuid.uuid4())
            new_user = Users(
                email=email,
                password=password,
                fullname=fullname,
                cellphone=cellphone,
                token_email=token_email,
                language_id=language_id,
                user_verified=0,
                role_id=role_id,
                created_at=datetime.now(),
            )

            db.session.add(new_user)
            db.session.commit()

            mail = configure_mail(current_app)
            isSend = send_email(mail, email, None, token_email)

            if not isSend:
                return {
                    "message": "Usuario registrado exitosamente, pero no se pudo enviar el correo de bienvenida.",
                    "success": True,
                }, 400

            return {
                "message": "Usuario registrado exitosamente, porfavor revise su correo",
                "success": True,
            }, 201

        except Exception as e:
            print(e)
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def verify_user(cls, token):
        try:
            user = Users.query.filter_by(token_email=token).first()

            if not user:
                return {
                    "error": "El usuario no existe o ya ha sido verificado",
                    "success": False,
                }, 400

            user.token_email = None
            user.user_verified = 1
            db.session.commit()

            return {
                "message": "Usuario verificado exitosamente.",
                "email": user.email,
                "success": True,
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500
