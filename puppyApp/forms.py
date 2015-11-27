from wtforms import Form, BooleanField, StringField, validators, IntegerField, FloatField


class NewPuppyForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    gender = StringField('Gender', [validators.Length(min=4, max=35)])
    weight = FloatField('Weight', [validators.NumberRange(min=0.1, max=500, message='wth!')])