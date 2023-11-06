from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.db_pg import db


class Messages(db.Model):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    uuid_conversation = Column(String, nullable=False)
    id_user_sender = Column(String)
    id_user_receiver = Column(String)
    message_text = Column(String)
    message_traslated_text = Column(String)
    message_read = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    read_at = Column(DateTime)

    def __init__(
        self,
        uuid_conversation,
        id_user_sender,
        id_user_receiver,
        message_text,
        message_traslated_text,
        message_read,
        created_at=None,
        read_at=None,
    ):
        self.uuid_conversation = uuid_conversation
        self.id_user_sender = id_user_sender
        self.id_user_receiver = id_user_receiver
        self.message_text = message_text
        self.message_traslated_text = message_traslated_text
        self.message_read = message_read
        self.created_at = created_at
        self.read_at = read_at

    def to_dict(self):
        return {
            "id": self.id,
            "uuid_conversation": self.uuid_conversation,
            "id_user_sender": self.id_user_sender,
            "id_user_receiver": self.id_user_receiver,
            "message_text": self.message_text,
            "message_traslated_text": self.message_traslated_text,
            "message_read": self.message_read,
            "created_at": self.created_at,
            "read_at": self.read_at,
        }
