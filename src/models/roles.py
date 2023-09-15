from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Roles(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name_role = Column(String(80))

    users = relationship("Users", back_populates="role")


# def insert_default_roles():
#     role1 = Roles(name_role="agent")
#     role2 = Roles(name_role="user")
#     db.session.add(role1)
#     db.session.add(role2)
#     db.session.commit()
