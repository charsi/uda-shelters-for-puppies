
from flask import (
    Flask, render_template, url_for,
    request, redirect, flash, jsonify
)
from flask_util_js import FlaskUtilJs
app = Flask(__name__)

fujs = FlaskUtilJs(app)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Puppy, Shelter, Adopter
import queries

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.Bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def shelters():
    shelters = session.query(Shelter)
    return render_template('sheltersindex.html', shelters=shelters)


@app.route('/shelter/<int:shelter_id>/')
def shelterPage(shelter_id):
    # get the shelter object
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    # get all puppies housed at the shelter
    puppies = session.query(Puppy).filter_by(shelter_id=shelter_id)
    return render_template('shelter.html', shelter=shelter, puppies=puppies)


@app.route('/puppy/<int:puppy_id>/')
def puppyProfile(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template('puppyprofile.html', puppy=puppy)


@app.route('/adoptapuppy/', methods=['GET', 'POST'])
def adoptPuppy():
    if request.method == 'POST':
        if request.values['id']:
            puppy = session.query(Puppy).filter_by(id=request.form['id']).one()
            return puppy.name


@app.route('/adopter/<int:adopter_id>/')
def adopterProfile(adopter_id):
    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template('adopterprofile.html', adopter=adopter)

if __name__ == '__main__':
    # dummy secret key; required only for message flashing
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
