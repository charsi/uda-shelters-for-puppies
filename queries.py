from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Puppy, Shelter, Profile
from sqlalchemy import asc, desc
from datetime import date
import dateutil.relativedelta

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.Bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

puppiesByName = (
    session.query(Puppy)  # returns Puppy objects as a tuple?
    .order_by(asc(Puppy.name))  # order by name
)

if __name__ == "__main__":
    for puppy in puppiesByName.all():
        print puppy.name

    today = date.today()
    sixMonthsAgo = today - dateutil.relativedelta.relativedelta(months=6)

    youngPuppies = (
        session.query(Puppy)  # returns Puppy objects
        .order_by(desc(Puppy.dateOfBirth))  # order by dob
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)

    )

    for puppy in youngPuppies.all():
        print "%s\tDOB: %s" % (puppy.name, puppy.dateOfBirth)

    puppiesByWeight = (
        session.query(Puppy)  # returns Puppy objects as a tuple?
        .order_by(asc(Puppy.weight))  # order by weight
    )
    for puppy in puppiesByWeight.all():
        print "%s\tweight: %s kg" % (puppy.name, round(puppy.weight, 2))

    puppiesByShelter = (
        session.query(Puppy)  # returns Puppy objects as a tuple?
        .order_by(asc(Puppy.shelter_id))
        .order_by(asc(Puppy.name))  # order by name
        # .group_by(Puppy.shelter_id)
    )

    for puppy in puppiesByShelter.all():
        print "%s\tshelter id: %s" % (puppy.name, puppy.shelter_id)


def findShelterbyId(id):
    return session.query(Shelter).filter_by(id=id).one()


def addPuppy(puppyObj):
    """adds a new puppy to the database
    Args: an object of class puppy
    """
    shelter_id = puppyObj.shelter_id
    shelter = findShelterbyId(shelter_id)
    if shelter.current_occupancy >= shelter.maximum_capacity:
        raise Exception("Shelter already at maximum capacity. Please try another one")
    shelter.current_occupancy += 1
    session.add(shelter)
    session.add(puppyObj)
    session.commit()
