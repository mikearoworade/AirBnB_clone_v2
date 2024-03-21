#!/usr/bin/python3
"""Contains the class DBStorage"""

import models
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

"""handles long term storage of all class instances"""
classes = {
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }

class DBStorage:
    """interaacts with the MySQL database"""

    """handles long term storage of all class instances"""
    

    """handles storage for database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object
         creates the engine self.__engine
         """
        HBNB_MYSQL_USER = os.environ.get('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.environ.get('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.environ.get('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.environ.get('HBNB_MYSQL_DB')
        HBNB_ENV = os.environ.get('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session
        returns a dictionary of all objects
        """
        obj_dict = {}
        for clas in classes:
            if cls is None or cls is classes[clas] or cls is clas:
                a_query = self.__session.query(classes[clas]).all()
                for obj in a_query:
                    obj_key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[obj_key] = obj
        return obj_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """retrieves one object based on class name and id"""
        if cls not in classes.values():
            return None

        all_obj = self.all(cls)
        for value in all_obj.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """returns the count of all objects in storage"""
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count
