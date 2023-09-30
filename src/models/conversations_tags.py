from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
import uuid

from src.database.db_pg import db


class Conversations_Tags(db.Model):
    __tablename__ = "conversations_tags"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    tag = relationship(
        "Tags",
        back_populates="conversations_tags",
    )

    conversation = relationship(
        "Conversations",
        back_populates="conversations_tags",
    )
