
from flask import Blueprint, request, jsonify

from src.middleware.token_required import token_required
from src.services.common.dashboard_service import DashBoardService

dashboard_admin_bp = Blueprint("admin/dashboard", __name__)


@dashboard_admin_bp.route("/get_requests_for_month", methods=["GET"])
def get_requests_for_month():
    try:
        response, status = DashBoardService.count_requests_by_month()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    
@dashboard_admin_bp.route("/get_count_clients_by_month", methods=["GET"])
def get_count_clients_by_month():
    try:
        response, status = DashBoardService.count_clients_by_month()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    
@dashboard_admin_bp.route("/get_total_attended_chats", methods=["GET"])
def get_total_attended_chats():
    try:
        response, status = DashBoardService.total_attended_chats()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    
@dashboard_admin_bp.route("/get_percentage_of_users_by_role", methods=["GET"])
def get_percentage_of_users_by_role():
    try:
        response, status = DashBoardService.percentage_of_users_by_role()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    
@dashboard_admin_bp.route("/get_count_chats_by_hour", methods=["GET"])
def get_count_chats_by_hour():
    try:
        response, status = DashBoardService.count_chats_by_hour()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    
@dashboard_admin_bp.route("/get_total_of_users", methods=["GET"])
def get_total_of_users():
    try:
        response, status = DashBoardService.total_of_users()
        return jsonify(response), status
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    
