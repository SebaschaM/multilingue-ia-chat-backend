from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db_pg import db


class Sessions(db.Model):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(128))
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    ip_address = Column(String(80))
    user_agent = Column(String(80))

    user = relationship("Users", back_populates="sessions", overlaps="user_sessions")

    def to_dict():
        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "token": self.token,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
        }
