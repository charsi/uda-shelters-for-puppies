from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Puppy, Shelter
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

for puppy in puppiesByName.all():
    print puppy.name

today = date.today()
sixMonthsAgo = today - dateutil.relativedelta.relativedelta(months=6)

youngPuppies = (
    session.query(Puppy)  # returns Puppy objects
    .order_by(desc(Puppy.dateOfBirth))  # order by name
    .filter(Puppy.dateOfBirth >= sixMonthsAgo)

)

for puppy in youngPuppies.all():
    print "%s\tDOB: %s" % (puppy.name, puppy.dateOfBirth)


puppiesByWeight = (
    session.query(Puppy)  # returns Puppy objects as a tuple?
    .order_by(asc(Puppy.weight))  # order by name
)
for puppy in puppiesByWeight.all():
    print "%s\tweight: %s kg" % (puppy.name, round(puppy.weight, 2))
