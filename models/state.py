#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
import models
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="delete", backref="state")

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """ Get a list of related Cities inside the state"""
            obj_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    obj_list.append(city)
            return obj_list
