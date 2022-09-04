from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.fields.numeric import IntegerField
from wtforms.validators import Length, DataRequired



##########   PASSENGER FILL-UP FORM FUNCTION    #############


class SignUpForm(FlaskForm):
    name = StringField('Shopkeeper Name*', validators=[DataRequired(), Length(max = 20)])
    shopname = StringField('Enter Shop Name*', validators=[DataRequired(), Length(max = 30)])
    email = StringField('Enter your Email*', validators=[DataRequired(), Length(max = 50)])
    mobile = StringField('Mobile Number*',validators=[DataRequired(), Length(max = 10,min = 10)])
    addressline1 = StringField('Address Line 1*', validators=[DataRequired(), Length(max = 50)] )
    city = StringField('City*', validators=[DataRequired(), Length(max = 10)] )
    pincode = StringField('Enter Pincode*', validators=[DataRequired(), Length(max = 8)])
    submit = SubmitField('Next')
    
    
##########   RECIEVER FILL-UP FORM FUNCTION    ##############


class RecSignUpForm(FlaskForm):
    name = StringField('Customer Name*', validators=[DataRequired(), Length(max = 20)])
    age = StringField('Enter your age*', validators=[DataRequired(), Length(max = 3)])
    mobile = StringField('Mobile Number*',validators=[DataRequired(), Length(max = 10,min = 10)])
    submit = SubmitField('Submit')
    

class BookName(FlaskForm):
    bookname = StringField('Book Name*', validators=[DataRequired(), Length(max = 50)])
    isbn = StringField('ISBN No.*', validators=[DataRequired(), Length(max = 13,min = 13)])
    available  = StringField('No. of Books Available*', validators=[DataRequired(), Length(max = 50)])
    rented = StringField('No. of Books Rented*',validators=[DataRequired(), Length(max = 50)])
    price = StringField('Price of the mentioned book*', validators=[DataRequired(), Length(max = 50)] )
    category= StringField('Category*', validators=[DataRequired(), Length(max = 10)] )
    submit = SubmitField('Submit')