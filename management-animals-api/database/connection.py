from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")


# Motor de bd
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

"""
Cada instancia de la clase SessionLocal será una sesión de 
base de datos. La clase en sí no es una sesión de base de datos todavía.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""
Posteriormente heredaremos de esta clase para crear 
cada uno de los modelos o clases de base de datos (los modelos ORM):

"""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")


# Motor de bd
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

"""
Cada instancia de la clase SessionLocal será una sesión de 
base de datos. La clase en sí no es una sesión de base de datos todavía.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""
Posteriormente heredaremos de esta clase para crear 
cada uno de los modelos o clases de base de datos (los modelos ORM):

"""