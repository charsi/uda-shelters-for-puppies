import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

puppy_adopter_tbl = Table(
    'association', Base.metadata,
    Column('left_id', Integer, ForeignKey('puppy.id')),
    Column('right_id', Integer, ForeignKey('adopter.id'))
)


class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(180))
    city = Column(String(30))
    state = Column(String(30))
    zipCode = Column(Integer(30))
    website = Column(String(150))
    maximum_capacity = Column(Integer, default=0)
    current_occupancy = Column(Integer, default=0)


class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    dateOfBirth = Column(Date)
    gender = Column(String(10))
    weight = Column(Float)
    picture = Column(String(360))

    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

    profile = relationship("Profile", uselist=False, backref="puppy")
    adopter = relationship(
        "Adopter",
        secondary=puppy_adopter_tbl,
        backref="puppy"
    )


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    photo = Column(String(360))
    description = Column(String(360))
    splNeeds = Column(String(360))
    puppy_id = Column(Integer, ForeignKey('puppy.id'))


class Adopter(Base):
    __tablename__ = 'adopter'

    id = Column(Integer, primary_key=True)
    name = Column(String(360))

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
