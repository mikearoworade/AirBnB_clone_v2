#!/usr/bin/python3
"""Defines the Review class."""
import os
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

class Review(BaseModel, Base):
    """Represents a review for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table reviews.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Reviews.
        text (sqlalchemy String): The review description.
        place_id (sqlalchemy String): The review's place id.
        user_id (sqlalchemy String): The review's user id.
    """
    if STORAGE_TYPE == "db":
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    else:
        place_id = ""
        user_id = ""
        text = ""
