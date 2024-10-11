from flask_wtf import Form
from wtforms import StringField,TextAreaField, IntegerField,SubmitField,RadioField,SelectField
from wtforms.validators import InputRequired, Email

class SignUpForm(Form):
    name = StringField("Name",[InputRequired("Please enter name")])
    gender = RadioField('gender',choices=[('M','Male'), ('F','Female'),('O','Other')])
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    submit = SubmitField('Send')