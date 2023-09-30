from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db_pg import db


class Messages(db.Model):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    id_user_sender = Column(Integer)
    id_user_receiver = Column(Integer)
    message_text = Column(String)
    message_traslated_text = Column(String)
    message_read = Column(Integer)
    created_at = Column(DateTime)
    read_at = Column(DateTime)
