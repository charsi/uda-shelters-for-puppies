from flask import render_template, url_for, request, redirect, flash, jsonify

# import app from __init__.py
from puppyApp import app

from forms import NewPuppyForm

# FlaskUtilJs to allow url_for function in javascript
from flask_util_js import FlaskUtilJs
fujs = FlaskUtilJs(app)

# momentjs in jinja
from flask.ext.moment import Moment
moment = Moment(app)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Puppy, Shelter, Adopter

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.Bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

import queries
from datetime import datetime

# to be able to access external APIs
import urllib2


@app.route('/getpuppypic/')
def getPuppyPic():
    '''
    Returns a url to random image of puppies.
    Not currently being used by the app.
    '''
    url = "http://www.thepuppyapi.com/puppy?format=src"
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url


def updateShelterOccupancy():
    "Updates current_occupancy column for all shelters"
    shelters = session.query(Shelter)
    for shelter in shelters:
        shelter.current_occupancy = (
            # get all puppies which match the current shelter
            session.query(Puppy).filter_by(shelter_id=shelter.id).count()
        )
        session.add(shelter)
        session.commit()


@app.route('/shelter/<int:shelter_id>/newpuppy/', methods=['GET', 'POST'])
def newPuppy(shelter_id):
    form = NewPuppyForm(request.form)
    if request.method == 'POST' and form.validate():
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        if shelter.current_occupancy >= shelter.maximum_capacity:
            flash('Shelter already at maximum capacity. Please try \
                another one')
            # reload page and display the flash messaage
            return render_template(
                'newpuppy.html',
                form=form, shelter_id=shelter_id
            )
        shelter.current_occupancy += 1
        session.add(shelter)
        puppy = Puppy()
        puppy.name = form.name.data
        puppy.gender = form.gender.data
        puppy.weight = form.weight.data
        puppy.shelter_id = shelter_id
        puppy.dateOfBirth = datetime.strptime(form.dob.data, '%Y-%m-%d').date()
        session.add(puppy)
        session.commit()
        flash('new puppy added', 'warn')
        # Go back to shelter page
        return redirect(url_for('shelterPage', shelter_id=shelter_id))
    else:
        # Show form
        return render_template(
            'newpuppy.html',
            form=form, shelter_id=shelter_id
        )


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
    imgurl = getPuppyPic()
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
