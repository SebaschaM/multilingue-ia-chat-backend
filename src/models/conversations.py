from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
import uuid

from src.database.db_pg import db


class Conversations(db.Model):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False, default=str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.uuid"))
    client_conversation_id = Column(String, ForeignKey("clients.uuid"))
    reason_contact = Column(String, nullable=True)
    state = Column(Integer, nullable=False, default=0)  # 1: active, 0: finished

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
        reason_contact=None,
        state=1,
        uuid=None,
    ):
        self.user_id = user_id
        self.client_conversation_id = client_conversation_id
        self.reason_contact = reason_contact
        self.state = state
        self.uuid = uuid

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "user": self.user.to_dict(),
            "client_conversation": self.client.to_dict(),
            "reason_contact": self.reason_contact,
            "state": self.state,
        }
