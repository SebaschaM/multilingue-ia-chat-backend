from flask import Blueprint, request, jsonify

from src.services.admin.request_admin_service import RequestAdminService
from src.middleware.token_required import token_required


request_admin_bp = Blueprint("admin/request", __name__)


@request_admin_bp.route("/register-request", methods=["POST"])
def register_request():
    try:
        data = request.get_json()
        request_fields = [
            "date_attention",
            "reason",
            "destination_area",
            "user_id",
            "client_id",
        ]

        for field in request_fields:
            if field not in data:
                return jsonify({"error": f"{field} required"}), 400

        response, status = RequestAdminService.register_request(data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@request_admin_bp.route("/get-requests", methods=["GET"])
def get_requests():
    try:
        response, status = RequestAdminService.get_requests()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@request_admin_bp.route("/change-state-request", methods=["PUT"])
def change_state_request():
    try:
        data = request.get_json()
        request_fields = [
            "request_id",
            "status_id",
        ]

        for field in request_fields:
            if field not in data:
                return jsonify({"error": f"{field} required"}), 400

        response, status = RequestAdminService.change_state_request(data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
