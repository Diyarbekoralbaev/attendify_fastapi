# models/client_model.py
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from database import Base
from datetime import datetime


class ClientsModel(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    image = Column(Text, nullable=False)
    first_seen = Column(String(80), nullable=False)
    last_seen = Column(String(80), nullable=False)
    visit_count = Column(Integer, nullable=False, default=1)
    gender = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "visit_count": self.visit_count,
            "gender": self.gender,
            "age": self.age
        }


class ClientVisitHistoryModel(Base):
    __tablename__ = "client_visit_history"
    id = Column(Integer, primary_key=True)
    datetime = Column(String(80), nullable=False)
    device_id = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "datetime": self.datetime,
            "device_id": self.device_id,
            "client_id": self.client_id
        }