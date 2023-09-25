from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Clients(db.Model):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(80))
    cellphone = Column(String(80))
    email = Column(String(80), unique=True, nullable=False)
    language = Column(String(80))
    created_at = Column(DateTime)

    conversations = relationship(
        "Conversations",
        # primaryjoin="Clients.id==Conversations.client_conversation_id",
        # backref="client_conversations",
        back_populates="client",
        # overlaps="client_conversations,conversations",
    )

    def __init__(
        self,
        email,
        fullname=None,
        cellphone=None,
        language=None,
        created_at=None,
    ):
        self.email = email
        self.fullname = fullname
        self.cellphone = cellphone
        self.language = language
        self.created_at = created_at
