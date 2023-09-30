from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Request_Types(db.Model):
    __tablename__ = "request_types"

    id = Column(Integer, primary_key=True)
    request_type_name = Column(String(80))
    description = Column(String(80))

    requests = relationship("Requests", back_populates="request_type")
