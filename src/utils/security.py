import datetime
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


class Security:
    secret_key = os.getenv("SECRET_KEY")

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "email": authenticated_user.email,
            "fullname": authenticated_user.fullname,
        }

        # El metodo .encode encripta el payload y devuelve un objeto de tipo bytes
        return jwt.encode(payload, cls.secret_key, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if "Authorization" in headers.keys():
            authorization = headers["Authorization"]
            encoded_token = authorization.split(" ")[1]

            try:
                decoded_token = jwt.decode(
                    encoded_token, cls.secret_key, algorithms=["HS256"]
                )
                return {"success": True, "decoded_token": decoded_token}, 200

            except jwt.ExpiredSignatureError:
                return {"error": "El token ha expirado.", "success": False}, 401

            except jwt.InvalidTokenError:
                return {"error": "El token es inválido.", "success": False}, 401

        else:
            return {"error": "No se ha enviado un token.", "success": False}, 401
