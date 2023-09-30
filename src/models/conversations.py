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
    )
    user = relationship(
        "Users",
        back_populates="conversations",
    )

    conversations_tags = relationship(
        "Conversations_Tags", back_populates="conversation"
    )
