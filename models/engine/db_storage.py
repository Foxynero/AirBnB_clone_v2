#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
import models
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage():
    """new storge"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """squery database session"""
        all_dict = {}
        for itr in classes:
            if cls is None or cls == itr:
                objs = self.__session.query(classes[itr]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    all_dict[key] = obj
        return (all_dict)

    def new(self, obj):
        """add new obj"""
        if obj is not None:
            self.__session.add(obj)
            self.save()

    def save(self):
        """commit changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj if exists"""
        if obj is not None:
            del obj
            self.save()

    def reload(self):
        """reload"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ calls close() on the class Session """
        self.__session.close()
