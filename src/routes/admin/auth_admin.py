from flask import Blueprint, request, jsonify

from src.services.admin.auth_admin_service import AuthAdminService
from src.middleware.token_required import token_required


auth_admin_bp = Blueprint("admin/auth", __name__)


@auth_admin_bp.route("/verify-email-exists", methods=["POST"])
def verify_email_exists():
    try:
        email = request.json.get("email")
        if not email:
            return jsonify({"error": "Correo electrónico requerido"}), 400

        response, status = AuthAdminService.verify_email_exists(email)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@auth_admin_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Correo y contraseña requeridos"}), 400

    response, status = AuthAdminService.login_user(email, password)
    return jsonify(response), status


@auth_admin_bp.route("/register", methods=["POST"])
def register():
    try:
        user_data = request.get_json()

        required_fields = [
            "email",
            "password",
            "fullname",
            "cellphone",
            "language_id",
            "role_id",
        ]
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"El campo '{field}' es requerido."}), 400

        response, status = AuthAdminService.register_user(user_data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@auth_admin_bp.route("/verify-email", methods=["GET"])
def verify_user():
    try:
        token = request.args.get("token")
        if not token:
            return jsonify({"error": "Token requerido"}), 400

        response, status = AuthAdminService.verify_user(token)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
