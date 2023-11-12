# Database
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid

from src.database.db_pg import db
from src.models.users import Users
from src.utils.security import Security
from src.utils.send_mail import send_email, configure_mail
from src.utils.validations import Validations


class UserAdminService:
    @classmethod
    def get_users(cls):
        try:
            users = Users.query.all()
            users_dict = [user.to_dict() for user in users]
            return {
                "users": users_dict,
                "success": True,
            }, 200
        except Exception as e:
            print(e)
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def register_user(cls, user_data):
        try:
            email = user_data["email"]
            password = generate_password_hash(user_data["password"])
            fullname = user_data["fullname"]
            cellphone = user_data["cellphone"]
            language_id = user_data["language_id"]
            role_id = user_data["role_id"]

            isValidEmail = Validations.validateEmail(email)
            if not isValidEmail:
                return {
                    "error": "El correo electrónico no es válido",
                    "success": False,
                }, 400

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
    def delete_user(cls, user_id):
        try:
            user = Users.query.filter_by(uuid=user_id).first()
            if not user:
                return {
                    "error": "El usuario no existe",
                    "success": False,
                }, 400

            db.session.delete(user)
            db.session.commit()

            return {
                "message": "Usuario eliminado exitosamente",
                "success": True,
            }, 200

        except Exception as e:
            print(e)
            return {
                "error": str(e),
                "success": False,
            }, 500

    @classmethod
    def update_user(cls, user_data):
        try:
            user_id = user_data["user_id"]
            fullname = user_data["fullname"]
            cellphone = user_data["cellphone"]
            language_id = user_data["language_id"]
            role_id = user_data["role_id"]
            password = user_data["password"]

            user = Users.query.filter_by(uuid=user_id).first()
            if not user:
                return {
                    "error": "El usuario no existe",
                    "success": False,
                }, 400

            user.password = generate_password_hash(password)
            user.fullname = fullname
            user.cellphone = cellphone
            user.language_id = language_id
            user.role_id = role_id

            db.session.commit()

            return {
                "message": "Usuario actualizado exitosamente",
                "success": True,
            }, 200

        except Exception as e:
            print(e)
            return {
                "error": str(e),
                "success": False,
            }, 500
