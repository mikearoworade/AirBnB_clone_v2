#!/usr/bin/python3
"""Defines the BaseModel class."""
import os
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

"""Creates instance of Base if storage type is a database
    If not database storage, uses class Base
"""
if STORAGE_TYPE == "db":
    Base = declarative_base()
else:
    class Base:
        pass

tformat = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """Represents the BaseModel of the AirBnB clone project
    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    if STORAGE_TYPE == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Instantiation of a new BaseModel Class
        Args:
            *args: Unused.
            **kwargs (dict): key/value pairs of attributes.
        """
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at =  datetime.utcnow()

    def __set_attributes(self, attr_dict):
        """private: converts attr_dict values to python class attributes.
        setattr() function sets the value of the specified attribute of the specified object.
        """
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())

        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(attr_dict['created_at'], tformat)

        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['updated_at'], datetime):
            attr_dict['updated_at'] = datetime.strptime(attr_dict['updated_at'], tformat)

        if STORAGE_TYPE != 'db':
            attr_dict.pop('__class__', None)

        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        dictcopy = self.__dict__.copy()
        dictcopy.pop("_sa_instance_state", None)
        clname = type(self).__name__ #0R self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, dictcopy)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(tformat)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(tformat)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def bm_update(self, attr_dict=None):
        """
            updates the basemodel and sets the correct attributes
        """
        IGNORE = [
            'id', 'created_at', 'updated_at', 'email',
            'state_id', 'user_id', 'city_id', 'place_id'
        ]
        if attr_dict:
            updated_dict = {
                k: v for k, v in attr_dict.items() if k not in IGNORE
            }
            for key, value in updated_dict.items():
                setattr(self, key, value)
            self.save()

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
