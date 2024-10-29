from flask_wtf import FlaskForm
from wtforms import TextField,IntegerField, SubmitField, StringField, RadioField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, InputRequired


class EmployForm(FlaskForm):
  job_reason = TextField("Why do you want this job", validators=[DataRequired(), Length(min=5, max=500)])
  submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    name = StringField("Name",[InputRequired("Please enter name")])
    gender = RadioField('gender',choices=[('M','Male'), ('F','Female'),('O','Other')])
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    password = PasswordField('password',[InputRequired("Password Required")])
    admin = RadioField('Are you an admin?', choices = [('Y', 'Yes'), ('N', 'No')])
    submit = SubmitField('Send')

class Login(FlaskForm):
    email = StringField('email',[InputRequired("Please enter an email address"), Email("wrong format")])
    password = PasswordField('password',[InputRequired("Password Required")])
    submit = SubmitField('Send')

class AddProductForm(FlaskForm):
   product = StringField("Product:", [InputRequired("Please enter product")])
   price = IntegerField("Price: ", [NumberRange(1,100)])
   ingredients = StringField("Ingredients:", [InputRequired("Please enter in the ingredients")])
   image = StringField("Image:", [InputRequired("Image required")])
   description = StringField("Description", [InputRequired('Description required')])
   submit = SubmitField('Submit')