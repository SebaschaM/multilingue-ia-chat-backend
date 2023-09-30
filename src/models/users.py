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
    language_id = Column(Integer, ForeignKey("languages.id"))
    user_verified = Column(Integer, default=0)
    role_id = Column(Integer, ForeignKey("roles.id"))
    attempt_counter = Column(Integer, default=0)
    block_until = Column(DateTime)
    created_at = Column(DateTime)

    role = relationship("Roles", back_populates="users", uselist=False)
    sessions = relationship(
        # "Sessions", primaryjoin="Users.id==Sessions.user_id", backref="user_sessions"
        "Sessions",
        back_populates="user",
    )
    conversations = relationship(
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
        self.created_at = created_at

    def to_dict(self):
        return {
            "email": self.email,
            "fullname": self.fullname,
            "cellphone": self.cellphone,
            "token_email": self.token_email,
            "token_phone": self.token_phone,
            "language": {
                "id": self.language.id,
                "name": self.language.name_language,
                "code": self.language.code_language,
                "flag_img": self.language.flag_img,
            },
            "user_verified": self.user_verified,
            "role": {
                "id": self.role.id,
                "name": self.role.name_role,
            },
            "created_at": self.created_at,
        }
