from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

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
    created_at = Column(DateTime, default=datetime.now())

    request_type = relationship("Request_Types", back_populates="requests")

    status = relationship(
        "Statuses",
        back_populates="requests",
    )

    user = relationship(
        "Users",
        back_populates="requests",
    )

    client = relationship(
        "Clients",
        back_populates="requests",
    )

    def __init__(
        self,
        date_attention,
        reason,
        destination_area,
        request_type_id,
        status_id,
        user_id,
        client_id,
        created_at=None,
    ):
        self.date_attention = date_attention
        self.reason = reason
        self.destination_area = destination_area
        self.request_type_id = request_type_id
        self.status_id = status_id
        self.user_id = user_id
        self.client_id = client_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "date_attention": self.date_attention,
            "reason": self.reason,
            "destination_area": self.destination_area,
            "request_type_id": self.request_type_id,
            "status": self.status.to_dict(),
            "user": self.user.to_dict(),
            "client": self.client.to_dict(),
            "created_at": self.created_at,
        }
