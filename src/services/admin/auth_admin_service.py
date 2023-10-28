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
            isValidEmail = Validations.validateEmail(email)
            if not isValidEmail:
                return {
                    "error": "El correo electrónico no es válido",
                    "success": False,
                }, 400

            user = Users.query.filter_by(email=email).first()
            if user is None:
                return {
                    "error": "El correo electrónico no existe.",
                    "success": False,
                }, 401

            if user.block_until is not None:
                if user.block_until > datetime.now():
                    time_rest = user.block_until - datetime.now()
                    time_rest_minutes = time_rest.seconds // 60
                    time_rest_hours = time_rest_minutes // 60

                    if time_rest_minutes <= 60:
                        return {
                            "error": "La cuenta se encuentra bloqueada, intentelo en {} minutos.".format(
                                time_rest_minutes
                            ),
                            "success": False,
                        }, 401

                    return {
                        "error": "La cuenta se encuentra bloqueada, intentelo en {} hora(s).".format(
                            time_rest_hours
                        ),
                        "success": False,
                    }, 401

                else:
                    user.block_until = None
                    user.blocked = 0
                    db.session.commit()

            if user.blocked == 1:
                return {
                    "error": "El usuario ha sido bloqueado, intentelo mas tarde o contacte con el administrador.",
                    "success": False,
                }, 401

            if not check_password_hash(user.password, password):
                count_temp = 4
                user.attempt_counter += 1
                count_temp = cls.__counter_attempts(count_temp, user.attempt_counter)
                db.session.commit()

                if user.attempt_counter == 4:
                    user.block_until = datetime.now() + timedelta(minutes=5)
                    user.blocked = 1
                    db.session.commit()

                    return {
                        "error": "La cuenta se ha bloqueado por 5 minutos.",
                        "success": False,
                    }, 401

                elif user.attempt_counter == 8:
                    user.block_until = datetime.now() + timedelta(hours=1)
                    user.blocked = 1
                    db.session.commit()

                    return {
                        "error": "La cuenta se ha bloqueado por 1 hora.",
                        "success": False,
                    }, 401

                elif user.attempt_counter == 12:
                    user.block_until = datetime.now() + timedelta(days=1)
                    user.blocked = 1
                    user.attempt_counter = 0
                    db.session.commit()

                    return {
                        "error": "La cuenta se ha bloqueado por 1 día.",
                        "success": False,
                    }, 401

                return {
                    "error": "Correo electrónico o contraseña incorrectos.",
                    "success": False,
                    "intents": count_temp,
                }, 401

            if user.user_verified == 0:
                return {
                    "error": "El usuario no ha sido verificado.",
                    "success": False,
                }, 401

            encoded_token = Security.generate_token(user)
            user.attempt_counter = 0
            user.block_until = None
            user.last_login = datetime.now()
            db.session.commit()
            return {
                "message": "Inicio de sesión exitoso.",
                "user": user.to_dict(),
                "success": True,
                "jwt_token": encoded_token,
            }, 200

        except Exception as e:
            return {"error": "Ocurrió un error inesperado.", "success": False}, 500

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

    @staticmethod
    def __counter_attempts(counter_temp, counter_user):
        if counter_user >= 5 and counter_user < 9:
            counter_temp = 4 - (counter_user - 4)
            return counter_temp
        elif counter_user >= 9 and counter_user < 13:
            counter_temp = 4 - (counter_user - 8)
            return counter_temp
        else:
            counter_temp = counter_temp - counter_user
            return counter_temp
