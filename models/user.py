#!/usr/bin/python3
"""Defines the User class."""
import os
import hashlib
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

class User(BaseModel, Base):
    """Represents a user for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table users.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store users.
        email: (sqlalchemy String): The user's email address.
        password (sqlalchemy String): The user's password.
        first_name (sqlalchemy String): The user's first name.
        last_name (sqlalchemy String): The user's last name.
        places (sqlalchemy relationship): The User-Place relationship.
        reviews (sqlalchemy relationship): The User-Review relationship.
    """
    if STORAGE_TYPE == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
            instantiates user object
        """
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __set_password(self, pwd):
        """
            custom setter: encrypts password to MD5
        """
        secure = hashlib.md5()
        secure.update(pwd.encode("utf-8"))
        secure_password = secure.hexdigest()
        setattr(self, "password", secure_password)
