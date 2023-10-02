from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Languages(db.Model):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    code_language = Column(String(80))
    name_language = Column(String(80))
    flag_img = Column(String(80))

    users = relationship("Users", back_populates="language")
    clients = relationship("Clients", back_populates="language")

    def to_dict(self):
        return {
            "id": self.id,
            "code_language": self.code_language,
            "name_language": self.name_language,
            "flag_img": self.flag_img,
        }
