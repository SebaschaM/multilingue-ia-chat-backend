from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(80))
    cellphone = Column(String(80))
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    token_email = Column(String(128))
    token_phone = Column(String(128))
    language = Column(String(80))
    user_verified = Column(Integer, default=0)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime)

    role = relationship("Roles", back_populates="users", uselist=False)
    sessions = relationship(
        "Sessions", primaryjoin="Users.id==Sessions.user_id", backref="user_sessions"
    )
    conversations = relationship(
        "Conversations",
        back_populates="user",
        # primaryjoin="Users.id==Conversations.user_id",
        # backref="user_conversations",
        # overlaps="user_conversations,coknversations",
    )

    def __init__(
        self,
        email,
        password,
        fullname=None,
        cellphone=None,
        token_email=None,
        token_phone=None,
        language=None,
        user_verified=None,
        role_id=None,
        created_at=None,
    ):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.cellphone = cellphone
        self.token_email = token_email
        self.token_phone = token_phone
        self.language = language
        self.user_verified = user_verified
        self.role_id = role_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "email": self.email,
            "fullname": self.fullname,
            "cellphone": self.cellphone,
            "token_email": self.token_email,
            "token_phone": self.token_phone,
            "language": self.language,
            "user_verified": self.user_verified,
            "role_id": self.role_id,
            "created_at": self.created_at,
        }
