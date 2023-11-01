from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.db_pg import db


class Messages(db.Model):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    id_user_sender = Column(Integer)
    id_user_receiver = Column(Integer)
    message_text = Column(String)
    message_traslated_text = Column(String)
    message_read = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    read_at = Column(DateTime)

    def __init__(
        self,
        id_user_sender,
        id_user_receiver,
        message_text,
        message_traslated_text,
        message_read,
        created_at=None,
        read_at=None,
    ):
        self.id_user_sender = id_user_sender
        self.id_user_receiver = id_user_receiver
        self.message_text = message_text
        self.message_traslated_text = message_traslated_text
        self.message_read = message_read
        self.created_at = created_at
        self.read_at = read_at
