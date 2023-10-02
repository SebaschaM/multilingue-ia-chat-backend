from flask import Blueprint, request, jsonify

from src.services.client.request_client_service import RequestClientService


request_client_bp = Blueprint("client/request", __name__)


@request_client_bp.route("/register-request", methods=["POST"])
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

        response, status = RequestClientService.register_request(data)
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@request_client_bp.route("/get-requests", methods=["GET"])
def get_requests():
    try:
        response, status = RequestClientService.get_requests()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
