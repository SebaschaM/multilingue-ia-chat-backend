from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db_pg import db


class Contacts(db.Model):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    contact_id = Column(Integer, ForeignKey("users.id"))

    contact = relationship("Users", foreign_keys=[contact_id])
