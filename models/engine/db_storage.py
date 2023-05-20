#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Create the engine(self.__engine)
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"), getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv("HBNB_MYSQL_ENV") == "test":
            Base.metadata.drop_all()

    def all(self, cls=None):
        """
        Returns a dictionary
        """
        my_objects = dict()
        objects = ["State", "City", "User", "Place", "Review", "Amenity"]

        for objts in objects:
            for obj in self.__session.query(eval(objts)).all():
                my_objects[type(obj).__name__+"."+obj.id] = obj

        return(my_objects)

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        self.__session.add(obj)

    def save(self):
        """serialize the file path to JSON file path
        """
        self.__session.commit()

    def reload(self):
        """serialize the file path to JSON file path
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(expire_on_commit=False,
                                        bind=self.__engine))()

    def delete(self, obj=None):
        """
        Deletes an object from objects
        """
        if obj:
            self.__session.delete(obj)
    
    def close(self):
        """more methods"""
        self.__session.close()
