#!/usr/bin/python3
"""Defines the Amenity class."""
import os
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

class Amenity(BaseModel, Base):
    """Represents an Amenity for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table amenities.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Amenities.
        name (sqlalchemy String): The amenity name.
        place_amenities (sqlalchemy relationship): Place-Amenity relationship.
    """
    if STORAGE_TYPE == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        places = relationship("Place", secondary="place_amenity", back_populates="amenities", cascade="delete")

    else:
        name = ""
