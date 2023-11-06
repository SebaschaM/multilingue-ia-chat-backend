from flask import Blueprint, request, jsonify

from src.services.common.message_service import MessageService
from src.middleware.token_required import token_required


messages_admin_bp = Blueprint("admin/messages", __name__)


@messages_admin_bp.route("/get-all-messages", methods=["GET"])
def get_all_messages():
    try:
        response = MessageService.get_all_messages()
        return jsonify(response)
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@messages_admin_bp.route(
    "/get-user-messages/<string:uuid_conversation>", methods=["GET"]
)
def get_user_messages(uuid_conversation):
    try:
        response = MessageService.get_messages_by_user(uuid_conversation)
        return jsonify(response)
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500


@messages_admin_bp.route("/get-user-conversations/<string:id_user>", methods=["GET"])
def get_user_conversations(id_user):
    try:
        response = MessageService.get_conversations_by_id_user(id_user)
        return jsonify(response)
    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
