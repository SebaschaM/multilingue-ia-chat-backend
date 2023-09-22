# Database
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from src.database.db_pg import db
from src.models.users import Users
from src.utils.security import Security
from src.utils.send_mail import send_email, configure_mail


class AuthService:
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
    def register_user_no_full(cls, user_data):
        try:
            email = user_data["email"]
            password = generate_password_hash(user_data["password"])

            if Users.query.filter_by(email=email).first():
                return {
                    "error": "El usuario ya existe.",
                    "success": False,
                }, 400

            token_email = str(uuid.uuid4())
            new_user = Users(
                email=email,
                password=password,
                token_email=token_email,
                name=None,
                lastname=None,
                date_of_birth=None,
                cellphone=None,
                token_phone=None,
                language="es",
                user_verified=0,
                role_id=2,
                created_at="2021-01-01 00:00:00",
            )
            db.session.add(new_user)
            db.session.commit()

            mail = configure_mail(current_app)
            isSend = send_email(mail, email, None, token_email)
            print("token", token_email)

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
    def register_user(cls, user_data):
        try:
            email = user_data["email"]
            # password = generate_password_hash(user_data["password"])
            name = user_data["name"]
            lastname = user_data["lastname"]
            date_of_birth = user_data["date_of_birth"]
            cellphone = user_data["cellphone"]

            user = Users.query.filter_by(email=email).first()

            if not user:
                return {
                    "error": "El usuario no existe.",
                    "success": False,
                }, 400

            # token_email = str(uuid.uuid4())
            # update
            user.name = name
            user.lastname = lastname
            user.date_of_birth = date_of_birth
            user.cellphone = cellphone
            # user.password = password
            # user.token_email = token_email
            db.session.commit()

            # mail = configure_mail(current_app)
            # isSend = send_email(mail, email, name, token_email)

            # if not isSend:
            #     return {
            #         "message": "Usuario registrado exitosamente",
            #         "success": True,
            #     }, 400

            return {
                "message": "Usuario registrado exitosamente.",
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
