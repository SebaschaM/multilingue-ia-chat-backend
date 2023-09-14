from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db_pg import db


class Messages(db.Model):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    id_user_sender = Column(Integer, ForeignKey("users.id"))
    id_user_receiver = Column(Integer, ForeignKey("users.id"))
    message_text = Column(String)
    created_at = Column(DateTime)
    read_at = Column(DateTime)

    user_sender = relationship(
        "Users", back_populates="messages_sender", foreign_keys=[id_user_sender]
    )
