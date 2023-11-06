from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from src.database.db_pg import db


class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False, default=str(uuid.uuid4()), unique=True)
    fullname = Column(String(80))
    cellphone = Column(String(80))
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    token_email = Column(String(128))
    token_phone = Column(String(128))
    language_id = Column(Integer, ForeignKey("languages.id"))
    user_verified = Column(Integer, default=0)
    role_id = Column(Integer, ForeignKey("roles.id"))
    attempt_counter = Column(Integer, default=0)
    block_until = Column(DateTime)
    blocked = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())
    last_login = Column(Date)

    role = relationship("Roles", back_populates="users", uselist=False)
    sessions = relationship(
        # "Sessions", primaryjoin="Users.id==Sessions.user_id", backref="user_sessions"
        "Sessions",
        back_populates="user",
    )
    conversations_user = relationship(
        "Conversations",
        back_populates="user",
    )

    language = relationship(
        "Languages",
        back_populates="users",
    )

    requests = relationship(
        "Requests",
        back_populates="user",
    )

    def __init__(
        self,
        email,
        password,
        fullname=None,
        cellphone=None,
        token_email=None,
        token_phone=None,
        language_id=None,
        user_verified=None,
        role_id=None,
        attempt_counter=None,
        block_until=None,
        blocked=None,
        created_at=None,
    ):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.cellphone = cellphone
        self.token_email = token_email
        self.token_phone = token_phone
        self.language_id = language_id
        self.user_verified = user_verified
        self.role_id = role_id
        self.attempt_counter = attempt_counter
        self.block_until = block_until
        self.blocked = blocked
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.uuid,
            # "uuid": self.uuid,
            "email": self.email,
            "fullname": self.fullname,
            "cellphone": self.cellphone,
            "token_email": self.token_email,
            "token_phone": self.token_phone,
            "language": self.language.to_dict(),
            "user_verified": self.user_verified,
            "role": self.role.to_dict(),
            "attempt_counter": self.attempt_counter,
            "block_until": self.block_until,
            "blocked": self.blocked,
            "created_at": self.created_at,
        }
