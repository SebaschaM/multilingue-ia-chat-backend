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
    def login_user(cls, email, password):
        try:
            user = Users.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return {"error": "Correo electrónico o contraseña incorrectos."}, 401

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
            email = user_data["email"]
            password = generate_password_hash(user_data["password"])
            name = user_data["name"]
            lastname = user_data["lastname"]
            date_of_birth = user_data["date_of_birth"]
            cellphone = user_data["cellphone"]

            if Users.query.filter_by(email=email).first():
                return {"error": "El usuario ya existe."}, 400

            token_email = str(uuid.uuid4())
            new_user = Users(
                email=email,
                password=password,
                name=name,
                lastname=lastname,
                date_of_birth=date_of_birth,
                cellphone=cellphone,
                token_email=token_email,
                token_phone=None,
                language="es",
                user_verified=0,
                role_id=2,
                created_at="2021-01-01 00:00:00",
            )
            db.session.add(new_user)
            db.session.commit()

            mail = configure_mail(current_app)
            isSend = send_email(mail, email, name, token_email)

            if not isSend:
                return {
                    "message": "Usuario registrado exitosamente, pero no se pudo enviar el correo de bienvenida.",
                    "success": True,
                }, 400

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
                return {"error": "El usuario no existe o ya ha sido verificado"}, 400

            user.token_email = None
            user.user_verified = 1
            db.session.commit()

            return {
                "message": "Usuario verificado exitosamente.",
                "success": True,
            }, 200

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }, 500
