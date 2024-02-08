from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata_obj = MetaData()

'''
A `Base` class that inherits from a declarative base object 
which combines a metadata container and a mapper that maps our class to a database table. 
It also maps instances of the class to records in that table if they have been saved.
This base class will be inherited by all ORM tables.
'''


class Base(DeclarativeBase):
    pass
