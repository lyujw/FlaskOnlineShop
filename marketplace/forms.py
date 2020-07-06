# Form-related classes.
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FloatField, FormField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, AnyOf, NumberRange, Regexp
from wtforms import RadioField, StringField, SubmitField, SelectField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea

class PhoneDetails(FlaskForm):
    regex = "^\d{11}$"
    number = StringField("Contact Number", validators=[Regexp(regex, message="Please enter 11 phone number."), InputRequired('Please enter a contact number.')])
    

class AccountDetails(FlaskForm):
    regexusername = "[A-Za-z0-9_]+"
    user_name = StringField("Username", validators=[InputRequired('Please enter a username.'), Length(min=3, max=20), Regexp(regexusername, message="Please enter a username that only includes letters between A-Z or a-z, numbers between 0-9 or underscores.")])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email address."), InputRequired('Please enter an email address.')])

class PasswordDetails(FlaskForm):
    # Linking two fields - password should be equal to data entered in confirmation field.
    password = PasswordField("Password", validators=[InputRequired('Please enter a password.'),
    EqualTo('confirm', message="Passwords should match.")])
    confirm = PasswordField("Please confirm your password", validators=[InputRequired('Please confirm your password.')])

# Login form.
class LoginForm(FlaskForm):
    user_name = StringField("Username", validators=[InputRequired('Please enter your username.')])
    password = PasswordField("Password", validators=[InputRequired('Please enter your password.')], render_kw={"a-value" : "b123"})
    submit = SubmitField("Login", render_kw={"submit-value" : "b123"})

# Registration form.
class RegisterForm(FlaskForm):
    account_details = FormField(AccountDetails)
    mobile_phone = FormField(PhoneDetails)
    password = FormField(PasswordDetails)
    # Submit button.
    submit = SubmitField("Register", render_kw={"submit2-value" : "b888"})


# Item creation form.
ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp', 'JPEG'}
class ItemCreationForm(FlaskForm):
    Currency = "^\$(?!0\.00)\d{1,3}(,\d{3})*(\.\d\d)?$"
    listing_title = StringField('Listing Title', validators=[InputRequired()])
    purchase_price = StringField('Price', validators=[InputRequired(message="Please enter a Selling price"),
                                            Regexp(Currency, message="Please enter a valid amount and currency e.g. '$30.00' or '$1,000.00'")])
    description = TextAreaField('Description', widget=TextArea(), validators=[InputRequired(), Length(min=1, max=1500)])
    game_condition = RadioField('Condition Of Game', choices=[('New','New'),('Preowned','Preowned')], default='New')
    game_release_date = DateField('Release Date', validators=[InputRequired("Please select a date")], format='%Y-%m-%d')
    game_genre = SelectField('Genre', choices=[(None, 'Please select game genre'), ('Action', 'Action'), ('Action-Adventure', 'Action-Adventure'), ('Adventure', 'Adventure',), ('Casual', 'Casual'),
    ('Party', 'Party'), ('Role-Playing', 'Role-Playing'), ('Simulation', 'Simulation'),
    ('Strategy', 'Strategy'), ('Sports', 'Sports'), ('MMO', 'MMO')])
    game_classification = SelectField('Classification', choices=[(None, 'Please select game classification'), ('Exempt', 'Exempt (E)'), ('General', 'General (G)'), ('Parental Guidance', 'Parental Guidance (PG)'), ('Mature', 'Mature (M)'), ('Mature Accompanied', 'Mature Accompanied (MA)'), ('Restricted', 'Restricted (R 18+)')])
    game_platform = SelectField('Platform', validators=[InputRequired()], choices=[(None, 'Please select game platform'), ('Arcade Systems', 'Arcade Systems'), ('Atari', 'Atari'),
    ('Commodore 64', 'Commodore 64'), ('Nintendo', 'Nintendo'), ('Nintendo 64', 'Nintendo 64'), ('Nintendo 3DS', 'Nintendo 3DS'), ('Nintendo DS', 'Nintendo DS'),
    ('Nintendo Switch', 'Nintendo Switch'), ('Nintendo Wii', 'Nintendo Wii'), ('Nintendo Wii U', 'Nintendo Wii U'),  ('PC', 'PC'),
    ('Playstation 3', 'Playstation 3'), ('Playstation 4', 'Playstation 4'), ('Playstation Classic', 'Playstation Classic'), ('Playstation Vita', 'Playstation Vita'),
    ('SEGA', 'SEGA'), ('Super Nintendo', 'Super Nintendo'), ('Xbox 360', 'Xbox 360'), ('Xbox One', 'Xbox One')])
    listing_img_url = FileField('Upload Image', validators=[FileRequired(message='Image can not be empty'),
                                            FileAllowed(ALLOWED_FILE, message='File with incorrect format provided. .png, .jpg, .JPG, .PNG, .bmp and .JPEG are the supported file formats.')])
    submit = SubmitField("Create Listing")
