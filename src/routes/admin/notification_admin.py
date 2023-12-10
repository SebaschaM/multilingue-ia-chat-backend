from flask import Blueprint, request

from src.services.admin.notification_service import NotificationAdminService


notification_admin_bp = Blueprint("admin/notification", __name__)


@notification_admin_bp.route("/register-notification", methods=["POST"])
def register_notification():
    try:
        data = request.get_json()
        return NotificationAdminService.register_notification(data)

    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500


@notification_admin_bp.route("/get-all-notification", methods=["GET"])
def get_notifications():
    try:
        return NotificationAdminService.get_notifications()

    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500


@notification_admin_bp.route("/get-active-notifications", methods=["GET"])
def get_notifications_active():
    try:
        return NotificationAdminService.get_notifications_active()

    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500


@notification_admin_bp.route("/update-notification/<int:id>", methods=["PUT"])
def update_notifications_active(id):
    try:
        data = request.get_json()
        return NotificationAdminService.update_notifications_active(id, data)

    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500


@notification_admin_bp.route("/delete-notification/<int:id>", methods=["DELETE"])
def delete_notifications_active(id):
    try:
        return NotificationAdminService.delete_notifications_active(id)

    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500
