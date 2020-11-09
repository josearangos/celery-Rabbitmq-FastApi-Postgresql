# Create SQLAlchemy models from the Base class
"""
SQLAlchemy usa el término "modelo" para referirse 
a estas clases e instancias que interactúan con la base de datos.
"""
from sqlalchemy import Boolean, Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from database.connection import Base

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime)
    last_modified = Column(DateTime)
    danger = Column(Boolean)
    name = Column(String)
    wild = Column(Boolean)
    notify = Column(Boolean)


    #A type for datetime.datetime() objects.


