from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Roles(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name_role = Column(String(80))

    users = relationship("Users", back_populates="role")

    def to_dict(self):
        return {
            "id": self.id,
            "name_role": self.name_role,
        }
