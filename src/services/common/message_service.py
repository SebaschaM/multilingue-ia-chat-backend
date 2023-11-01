from src.database.db_pg import db
from src.models.conversations import Conversations
from src.models.messages import Messages


class MessageService:
    @classmethod
    def save_message(cls, data):
        try:
            message = Messages(
                id_user_sender=data["id_user_sender"],
                id_user_receiver=data["id_user_receiver"],
                message_text=data["message_text"],
                message_traslated_text=data["message_traslated_text"],
                message_read=data["message_read"],
            )

            db.session.add(message)
            db.session.commit()

            return {
                "message": "Request created successfully",
                "success": True,
            }, 201
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def get_all_messages(cls):
        try:
            requests = Requests.query.all()
            requests = [request.to_dict() for request in requests]
            return {"requests": requests}, 200
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500
