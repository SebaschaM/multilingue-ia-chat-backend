# Database
from src.database.db_pg import db
from src.models.user import User
from src.utils.security import Security


class AuthService:
    @classmethod
    def login_user(cls, email, password):
        try:
            user = User.query.filter_by(email=email).first()

            # Si el usuario no existe o la contraseña es incorrecta, devuelve un error
            # if not user or not check_password_hash(user.password, password):
            #     return {"error": "Correo electrónico o contraseña incorrectos."}, 401
            if not user or user.password != password:
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
            }

    @classmethod
    def register_user(cls, user_data):
        try:
            email = user_data["email"]
            password = user_data["password"]
            name = user_data["name"]
            lastname = user_data["lastname"]
            date_of_birth = user_data["date_of_birth"]
            cellphone = user_data["cellphone"]

            if User.query.filter_by(email=email).first():
                return {"error": "El usuario ya existe."}, 400

            new_user = User(
                email=email,
                password=password,
                name=name,
                lastname=lastname,
                date_of_birth=date_of_birth,
                cellphone=cellphone,
            )

            db.session.add(new_user)
            db.session.commit()

            return {
                "message": "Usuario registrado exitosamente.",
                "success": True,
            }, 201

        except Exception as e:
            return {
                "error": str(e),
                "success": False,
            }
