from flask import Blueprint, request, jsonify

from src.services.client.auth_client_service import AuthClientService


auth_client_bp = Blueprint("client/auth", __name__)


@auth_client_bp.route("/verify-email-exists", methods=["POST"])
def verify_email_exists():
    try:
        email = request.json.get("email")
        print(email)
        if not email:
            return jsonify({"error": "Correo electrónico requerido"}), 400

        response, status = AuthClientService.verify_email_exists(email)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@auth_client_bp.route("/register-no-full", methods=["POST"])
def register_no_full():
    try:
        client_data = request.get_json()

        required_fields = ["email", "fullname", "cellphone", "language_id"]
        for field in required_fields:
            if field not in client_data:
                return jsonify({"error": f"El campo '{field}' es requerido."}), 400

        response, status = AuthClientService.register_user_no_full(client_data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
