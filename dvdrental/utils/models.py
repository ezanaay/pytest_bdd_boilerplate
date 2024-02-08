from sqlalchemy import *
from sqlalchemy.orm import relationship
from lib.model.base import Base, metadata_obj
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
import sqlalchemy.types as types


class Actor(Base):
    __tablename__ = 'actor'
    actor_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    last_updated = Column(DateTime(timezone=True))


class Rental(Base):
    __tablename__ = 'rental'
    rental_id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'))
    rental_date = Column(Date)
    return_date = Column(Date)
    last_update = Column(Date)
    staff_id = Column(SMALLINT)
    customer_id = Column(SMALLINT)

    inventories = relationship('Inventory')


class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('film.film_id'))
    last_update = Column(Date)
    store_id = Column(SMALLINT)

    films = relationship('Film')


class Film(Base):
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(VARCHAR)
    description = Column(Text)
    last_update = Column(Date)
    rental_duration = Column(SMALLINT)



class FilmCategory(Base):
    __tablename__ = 'film_category'
    category_id = Column(Integer, primary_key=True)
    film_id = Column(SMALLINT, ForeignKey('film.film_id'))
    last_update = Column(Date)

    films = relationship('Film')


class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    last_update = Column(Date)

