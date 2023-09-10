# Database
from src.database.db_pg import db
from src.models.user import User


class AuthService:
    @classmethod
    def login_user(cls, username, password):
        try:
            user = User.query.filter_by(username=username).first()

            # Si el usuario no existe o la contraseña es incorrecta, devuelve un error
            # if not user or not check_password_hash(user.password, password):
            #     return {"error": "Correo electrónico o contraseña incorrectos."}, 401
            if not user or user.password != password:
                return {"error": "Correo electrónico o contraseña incorrectos."}, 401

            # Si el inicio de sesión es exitoso, devuelve el usuario
            return {"message": "Inicio de sesión exitoso.", "user": user.to_dict()}, 200

        except Exception as e:
            # Si ocurre un error, devuelve el mensaje de error
            return {"error": str(e)}, 500

    @classmethod
    def register_user(cls, username, password):
        try:
            # Si el usuario ya existe, devuelve un error
            if User.query.filter_by(username=username).first():
                return {"error": "El usuario ya existe."}, 400

            # Crea un nuevo usuario
            new_user = User(
                username=username,
                # password=generate_password_hash(password, method="sha256"),
                password=password,
            )

            # Guarda el nuevo usuario en la base de datos
            db.session.add(new_user)
            db.session.commit()

            # Si el registro es exitoso, devuelve el usuario
            return {
                "message": "Usuario registrado exitosamente.",
            }, 201

        except Exception as e:
            # Si ocurre un error, devuelve el mensaje de error
            return {"error": str(e)}, 500
