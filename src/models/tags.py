from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Tags(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name_tag = Column(String(80))

    conversations_tags = relationship("Conversations_Tags", back_populates="tag")
