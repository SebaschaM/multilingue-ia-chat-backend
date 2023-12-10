from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from src.database.db_pg import db


class Notifications(db.Model):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    message = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    state = Column(String(255), default="active")
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, message, start_time, end_time, state, created_at, updated_at):
        self.message = message
        self.start_time = start_time
        self.end_time = end_time
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
