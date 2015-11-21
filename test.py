from database_setup import Puppy
from queries import addPuppy

newPuppy = Puppy(name="nishil", shelter_id=1)

addPuppy(newPuppy)
