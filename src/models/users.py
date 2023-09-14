from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    lastname = Column(String(80))
    date_of_birth = Column(DateTime)
    cellphone = Column(String(80))
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    token_email = Column(String(128))
    token_phone = Column(String(128))
    language = Column(String(80))
    user_verified = Column(Integer, default=0)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime)

    role = relationship("Roles", back_populates="users")
    contacts = relationship(
        "Contacts", primaryjoin="Users.id==Contacts.user_id", backref="user"
    )
    sessions = relationship("Sessions", back_populates="user")
    messages_sender = relationship(
        "Messages", primaryjoin="Users.id==Messages.id_user_sender", backref="user"
    )

    def __init__(
        self,
        email,
        password,
        name,
        lastname,
        date_of_birth,
        cellphone,
        token_email=None,
        token_phone=None,
        language=None,
        user_verified=None,
        role_id=None,
        created_at=None,
    ):
        self.email = email
        self.password = password
        self.name = name
        self.lastname = lastname
        self.date_of_birth = date_of_birth
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
            "name": self.name,
            "lastname": self.lastname,
            "date_of_birth": self.date_of_birth,
            "cellphone": self.cellphone,
            "token_email": self.token_email,
            "token_phone": self.token_phone,
            "language": self.language,
            "user_verified": self.user_verified,
            "role_id": self.role_id,
            "created_at": self.created_at,
        }
