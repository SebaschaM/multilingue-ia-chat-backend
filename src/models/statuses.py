from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.db_pg import db


class Statuses(db.Model):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name_status = Column(String(80))
    description = Column(String(80))
    background_color = Column(String(80))
    color = Column(String(80))

    requests = relationship("Requests", back_populates="status")

    def to_dict(self):
        return {
            "id": self.id,
            "name_status": self.name_status,
            "description": self.description,
            "background_color": self.background_color,
            "color": self.color,
        }
