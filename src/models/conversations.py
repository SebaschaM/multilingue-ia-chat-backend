from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from src.database.db_pg import db


class Conversations(db.Model):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    rooom_name = Column(String)
    user_id = Column(String, ForeignKey("users.uuid"))
    client_conversation_id = Column(String, ForeignKey("clients.uuid"))
    reason_contact = Column(String, nullable=True)
    state = Column(Integer, nullable=False, default=0)  # 1: active, 0: finished
    created_at = Column(DateTime, default=datetime.now())

    client = relationship(
        "Clients",
        back_populates="conversations_client",
    )
    user = relationship(
        "Users",
        back_populates="conversations_user",
    )

    conversations_tags = relationship(
        "Conversations_Tags", back_populates="conversation"
    )

    def __init__(
        self,
        user_id,
        client_conversation_id,
        room_name=None,
        reason_contact=None,
        state=1,
        created_at=None,
    ):
        self.user_id = user_id
        self.client_conversation_id = client_conversation_id
        self.rooom_name = room_name
        self.reason_contact = reason_contact
        self.state = state
        self.uuid = str(uuid.uuid4())
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "room_name": self.rooom_name,
            "user": self.user.to_dict(),
            "client_conversation": self.client.to_dict(),
            "reason_contact": self.reason_contact,
            "state": self.state,
            "created_at": self.created_at,
        }
