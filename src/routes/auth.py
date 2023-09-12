from flask import Blueprint, request, jsonify
from src.models.user import User
from src.services.auth_service import AuthService
from src.database.db_pg import db
from src.middleware.token_required import token_required


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    response, status = AuthService.login_user(email, password)
    return jsonify(response), status


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        user_data = request.get_json()

        required_fields = [
            "name",
            "lastname",
            "date_of_birth",
            "cellphone",
            "email",
            "password",
        ]
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"El campo '{field}' es requerido."}), 400

        response, status = AuthService.register_user(user_data)
        return jsonify(response), status
    except Exception as e:
        return {"error": str(e)}, 500
