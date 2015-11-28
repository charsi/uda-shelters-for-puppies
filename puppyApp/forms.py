from wtforms import Form, BooleanField, SelectField, StringField, validators, IntegerField, FloatField
import re

regex = re.compile('[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])')

class NewPuppyForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    gender = SelectField('Gender', choices=[('Male', 'Male'),('Female', 'Female')])
    weight = FloatField('Weight', [validators.NumberRange(min=0.1, max=500, message='wth!')])
    dob = StringField('Date of birth', [validators.Regexp(regex)])
    