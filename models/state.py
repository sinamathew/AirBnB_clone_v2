#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
if not hasattr(BaseModel, 'metadata'):
    Base = declarative_base()


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    cities = relationship("City", cascade="all, delete-orphan")

    def get_cities(self):
        from models import storage
        return storage.all(City).filter(City.state_id == self.id)
