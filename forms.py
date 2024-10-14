from flask_wtf import Form
from wtforms import StringField,TextAreaField, IntegerField,SubmitField,RadioField,SelectField, PasswordField
from wtforms.validators import InputRequired, Email

class SignUpForm(Form):
    name = StringField("Name",[InputRequired("Please enter name")])
    gender = RadioField('gender',choices=[('M','Male'), ('F','Female'),('O','Other')])
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    password = PasswordField('password',[InputRequired("Password Required")])
    submit = SubmitField('Send')

class Login(Form):
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    password = PasswordField('password',[InputRequired("Password Required")])
    submit = SubmitField('Send')