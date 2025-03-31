from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    usertype = SelectField('User Type', choices=[('CL', 'Customer'), ('PL', 'Professional'), ('AL', 'Admin')]) 
    submit = SubmitField('Login')

class RegisterCusForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    pin_code = StringField('Pincode', validators=[DataRequired(), Length(max=6)])
    submit = SubmitField('Register')

class RegisterProForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    service_name = SelectField('Service Name', choices=[('Cleaning', 'Cleaning'), ('Installation', 'Installation'), ('Repair', 'Repair'), ('Electrical', 'Electrical'), ('Personal', 'Personal'), ('Outdoor', 'Outdoor'), ('Petcare', 'Petcare'), ('Renovation', 'Renovation'), ('Other', 'Other')])
    experience = StringField('Experience', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    pin_code = StringField('Pincode', validators=[DataRequired(), Length(max=6)])
    status =StringField('User Type',default="Pending", render_kw={"disabled":True,"hidden":True})
    submit = SubmitField('Register')

class ServiceForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[('Cleaning', 'Cleaning'), ('Installation', 'Installation'), ('Repair', 'Repair'), ('Electrical', 'Electrical'), ('Personal', 'Personal'), ('Outdoor', 'Outdoor'), ('Petcare', 'Petcare'), ('Renovation', 'Renovation'), ('Other', 'Other')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    base_price = DecimalField('Base Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    submit = SubmitField('Add Service')

class FeedbackForm(FlaskForm):
    service_name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Length(max=500)])
    submit = SubmitField('Submit Feedback')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), Length(max=100)])