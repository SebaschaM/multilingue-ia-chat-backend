from flask import Blueprint, request, jsonify

from src.services.admin.user_admin_service import UserAdminService
from src.middleware.token_required import token_required


user_admin_bp = Blueprint("admin/user", __name__)


@user_admin_bp.route("/get-users", methods=["GET"])
def get_users():
    try:
        response, status = UserAdminService.get_users()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@user_admin_bp.route("/get-user", methods=["GET"])
def get_user():
    try:
        user_uuid = request.json.get("user_uuid")
        if not user_uuid:
            return jsonify({"error": "ID de usuario requerido"}), 400

        response, status = UserAdminService.get_user(user_uuid)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@user_admin_bp.route("/register-user", methods=["POST"])
def register_user():
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

        response, status = UserAdminService.register_user(user_data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@user_admin_bp.route("/delete-user", methods=["DELETE"])
def delete_user():
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"error": "ID de usuario requerido"}), 400

        response, status = UserAdminService.delete_user(user_id)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@user_admin_bp.route("/update-user", methods=["PUT"])
def update_user():
    try:
        user_data = request.get_json()
        response, status = UserAdminService.update_user(user_data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
