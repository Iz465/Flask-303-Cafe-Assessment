from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField, SubmitField, StringField, RadioField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, InputRequired


class EmployForm(FlaskForm):
  first_name = TextField("First Name", validators=[DataRequired(), Length(min=2, max=30)])
  last_name = TextField("Last Name", validators=[DataRequired(), Length(min=2, max=30)])
  age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=16, max=100)])  
  address = TextField("Address", validators=[DataRequired()])
  phone_number = TextField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
  email = TextField("Email", validators=[DataRequired(), Email()])
  submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    name = StringField("Name",[InputRequired("Please enter name")])
    gender = RadioField('gender',choices=[('M','Male'), ('F','Female'),('O','Other')])
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    password = PasswordField('password',[InputRequired("Password Required")])
    submit = SubmitField('Send')

class Login(FlaskForm):
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    password = PasswordField('password',[InputRequired("Password Required")])
    submit = SubmitField('Send')
