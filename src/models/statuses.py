from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Statuses(db.Model):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name_status = Column(String(80))
    description = Column(String(80))
    background_color = Column(String(80))
    color = Column(String(80))

    request_types = relationship("Requests", back_populates="status")
