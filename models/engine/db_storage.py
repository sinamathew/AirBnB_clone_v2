#!/usr/bin/python3
""" Module for managing db storage for sqlalchemy """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.city import City
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.base_model import Base
from models.base_model import BaseModel


user = getenv("HBNB_MYSQL_USER")
password = getenv("HBNB_MYSQL_PWD")
host = getenv("HBNB_MYSQL_HOST")
database = getenv("HBNB_MYSQL_DB")
env_state = getenv("HBNB_ENV")
dialet = "mysql"
driver = "mysqldb"
connection_str = f"{dialet}+{driver}://{user}:{password}@{host}/{database}"


class DBStorage:
    """ class model for AirBNB clone """
    __engine = None
    __session = None

    def __init__(self):
        """ instance initializer """
        self.__engine = create_engine(connection_str, pool_pre_ping=True)
        if env_state == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
            query on the current database session
        """
        objs = []
        objs_dict = {}
        if cls is None:
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(State).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            objs.extend(self.__session.query(cls).all())
        for obj in objs:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            objs_dict[key] = obj
        return objs_dict

    def new(self, obj):
        """ create new entry in the database """
        self.__session.add(obj)

    def save(self):
        """ commit all changes to the database """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete an object from the database """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
            create all tables in the database (feature of SQLAlchemy)
            (WARNING: all classes who inherit from Base must be imported
            before calling Base.metadata.create_all(engine))
        """
        # create all tables in the database
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        # register the session factory
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ close the current session """
        self.__session.close()
