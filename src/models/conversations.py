from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
import uuid

from src.database.db_pg import db


class Conversations(db.Model):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False, default=str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    client_conversation_id = Column(Integer, ForeignKey("clients.id"))
    reason_contact = Column(String, nullable=False)
    state = Column(Integer, nullable=False, default=0)

    client = relationship(
        "Clients",
        back_populates="conversations",
        # foreign_keys=[client_conversation_id],
        # backref="conversations_client",
        # overlaps="conversations",
    )
    user = relationship(
        "Users",
        back_populates="conversations",
        # foreign_keys=[user_id],
        # backref="conversations_user",
        # overlaps="user_conversations",
    )
