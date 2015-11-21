import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    name = Column(String(80), nullable=False)
    address = Column(String(180))
    city = Column(String(30))
    state = Column(String(30))
    zipCode = Column(Integer(30))
    website = Column(String(150))
    id = Column(Integer, primary_key=True)


class Puppy(Base):
    __tablename__ = 'puppy'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    dateOfBirth = Column(Date)
    gender = Column(String(10))
    weight = Column(Float)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    picture = Column(String(360))
    shelter = relationship(Shelter)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
