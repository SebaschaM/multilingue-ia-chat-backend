from src.database.db_pg import db
from src.models.conversations import Conversations
from src.models.messages import Messages
from src.models.users import Users

from sqlalchemy import tablesample, func


class MessageService:
    @classmethod
    def get_random_user(cls):
        try:
            user = (
                Users.query.filter(Users.role_id == 1)
                .order_by(func.random())
                .limit(1)
                .first()
            )
            return user.to_dict()
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def save_conversation(cls, data):
        try:
            print("DATA: " + str(data))
            conversation_exists = Conversations.query.filter(
                (Conversations.user_id == data["user_id"])
                | (Conversations.user_id == data["client_conversation_id"])
            ).first()

            print("CONVERSATION EXISTS: " + str(conversation_exists))
            # None, conversation no existe

            if conversation_exists:
                conversation_uuid = conversation_exists.uuid
            else:
                new_conversation = Conversations(
                    user_id=data["user_id"],
                    client_conversation_id=data["client_conversation_id"],
                )

                db.session.add(new_conversation)
                db.session.commit()

                conversation_uuid = new_conversation.uuid

            return conversation_uuid
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def save_message(cls, data):
        print("DATA: " + str(data))
        try:
            message = Messages(
                uuid_conversation=data["uuid_conversation"],
                id_user_sender=data["id_user_sender"],
                id_user_receiver=data["id_user_receiver"],
                message_text=data["message_text"],
                message_traslated_text=data["message_traslated_text"],
                message_read=data["message_read"],
            )

            db.session.add(message)
            db.session.commit()

            return {
                "message": "Message created successfully",
                "success": True,
            }, 201
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def get_all_messages(cls):
        try:
            messages = Messages.query.all()
            return {"messages": messages.to_dict()}, 200
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def get_messages_by_user(cls, uuid_conversation):
        try:
            messages = Messages.query.filter(
                (Messages.uuid_conversation == uuid_conversation)
            ).all()
            messages_dict = [message.to_dict() for message in messages]
            return {"messages": messages_dict}
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500

    @classmethod
    def get_conversations_by_id_user(cls, id_user):
        try:
            conversations = Conversations.query.filter_by(user_id=id_user).all()
            conversations_dict = [
                conversation.to_dict() for conversation in conversations
            ]

            messages = (
                Messages.query.filter(
                    (Messages.uuid_conversation == Conversations.uuid)
                )
                .order_by(Messages.id.asc())
                .all()
            )

            ultimate_message_dict = messages[-1].to_dict()
            conversations_dict = [
                {
                    **conversation,
                    "last_message": ultimate_message_dict,
                }
                for conversation in conversations_dict
            ]

            return {
                "conversation": conversations_dict,
            }
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500
