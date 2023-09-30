from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Requests(db.Model):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    date_attention = Column(Date)
    reason = Column(String(80))
    destination_area = Column(String(80))
    request_type_id = Column(Integer, ForeignKey("request_types.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    created_at = Column(DateTime)

    request_type = relationship("Request_Types", back_populates="requests")

    status = relationship(
        "Statuses",
        back_populates="request_types",
    )

    user = relationship(
        "Users",
        back_populates="requests",
    )

    client = relationship(
        "Clients",
        back_populates="requests",
    )
