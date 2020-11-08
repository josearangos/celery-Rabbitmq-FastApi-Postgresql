# Create SQLAlchemy models from the Base class
"""
SQLAlchemy usa el término "modelo" para referirse 
a estas clases e instancias que interactúan con la base de datos.
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)