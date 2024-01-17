#!/from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from models.user import User


class Place(BaseModel, Base):
    __tablename__ = 'places'

    city_id = Column(String(60), nullable=False, foreign_key='cities.id')
    user_id = Column(String(60), nullable=False, foreign_key='users.id')
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)

    city = relationship("City", back_populates="places")
    user = relationship("User", back_populates="places")
