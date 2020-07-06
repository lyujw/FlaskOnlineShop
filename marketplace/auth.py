# Authentication functions.
from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from werkzeug.security import generate_password_hash,check_password_hash
from .forms import LoginForm,RegisterForm,AccountDetails,PhoneDetails,PasswordDetails
from flask_login import login_user, login_required,logout_user
from .models import User
from . import db
from datetime import date


# Create a blueprint.
bp = Blueprint('auth', __name__)

# For password storage.
from werkzeug.security import generate_password_hash,check_password_hash

# Route for logging in.
@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    error = None
    if (form.validate_on_submit() == True):
        # Get the username and password from the database.
        user_name = form.user_name.data
        password = form.password.data
        u1 = User.query.filter_by(user_name = user_name).first()
        # For if there is no user with that name.
        if u1 is None:
            error = 'Incorrect user name'
        # Check the password - notice password hash function.
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            # If all is good, set the login_user of flask_login to manage the user.
            login_user(u1)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(error, 'danger')
    return render_template('user.html', form = form, heading = 'Login')

# Route for user registration.
@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if (form.validate_on_submit() == True):
            # Get username, password and email from the form.
            uname = form.account_details.user_name.data
            pwd = form.password.password.data
            email = form.account_details.email_id.data
            account_creation_date = date.today()
            contact_number = form.mobile_phone.number.data
            # Check if a user by the same name already exists.
            u1 = User.query.filter_by(user_name=uname).first()
            if u1:
                flash('User name already exists, please login', 'warning')
                return redirect(url_for('auth.login'))
            # Doesn't store the password - creates password hash.
            pwd_hash = generate_password_hash(pwd)
            # Create a new user model object.
            new_user = User(user_name=uname, password_hash=pwd_hash, email_id=email, account_creation_date = account_creation_date, contact_number = contact_number)
            db.session.add(new_user)
            db.session.commit()
            u1 = User.query.filter_by(user_name=uname).first()
            login_user(u1)
            # Commit to the database and redirect to HTML page.
            return redirect(url_for('main.home'))
    # If there is a get message.
    else:
        return render_template('user.html', form=form, heading='Register')

# Route for logging out.
@bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.home'))
