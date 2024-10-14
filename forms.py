from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo 


class EmployForm(FlaskForm):
  name = TextField("Name", validators=[DataRequired(), Length(min=2, max=30)])
  age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=16, max=100)])
  gender = RadioField("Gender", choices=[('value', 'Male'), ('value', 'Female'), ('value', 'Other')])
  address = TextField("Address", validators=[DataRequired()])
  phone_number = TextField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
  email = TextField("Email", validators=[DataRequired(), Email()])
  submit = SubmitField('Submit')
