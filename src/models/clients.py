from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Clients(db.Model):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(80))
    cellphone = Column(String(80))
    email = Column(String(80), unique=True, nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"))
    created_at = Column(DateTime)

    conversations = relationship(
        "Conversations",
        back_populates="client",
    )

    language = relationship(
        "Languages",
        back_populates="clients",
    )

    requests = relationship(
        "Requests",
        back_populates="client",
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
