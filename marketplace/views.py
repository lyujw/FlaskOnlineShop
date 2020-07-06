# Functions for assorted other pages.
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Listing, Bid, Transaction, User
from .forms import ItemCreationForm
from datetime import datetime, date
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc

# Create a blueprint.
bp = Blueprint('main', __name__)

# Function for displaying the landing page.
@bp.route('/')
def home():
    listings = Listing.query.order_by(desc(Listing.date_posted), desc(Listing.id)).limit(8).all()
    if not current_user.is_authenticated:
        flash("Welcome to Australia's newest peer-to-peer marketplace. Register or log in now to unlock the full potential of Gamerverse!", 'warning')
    return render_template('Homepage.html', listings = listings)

# Function for displaying the page of owned listings.
@bp.route('/manageall')
@login_required
def allListings():
    listing = db.session.query(Listing.id, Listing.listing_title,
    Listing.date_posted, Listing.purchase_price, Listing.user_id).\
    filter(Listing.user_id == current_user.id).all()

    return render_template('manageall.html', listing=listing)

# Function for displaying the seller history page.
@bp.route('/sellerhistory')
@login_required
def history():
    listing = db.session.query(Listing.id, Listing.listing_title,
    Listing.date_posted, Listing.purchase_price, Listing.user_id,
    Transaction.purchase_date, User.id, User.user_name).\
    filter(Listing.id == Transaction.listing_id, User.id == Transaction.user_id,
    Listing.availability_status == 'Sold', Listing.user_id == current_user.id).all()

    return render_template('sellerhistory.html', listing=listing)

# Function for uploading images.
def check_upload_file(form):
    fp = form.listing_img_url.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/Images', secure_filename(filename))
    db_upload_path = '/static/Images/'+ secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# Function for the listing creation page.
@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    print('In create item')
    form = ItemCreationForm()
    if form.validate_on_submit():
        print("Form has been submitted successfully")
        db_file_path = check_upload_file(form)

        # Listing creation form.
        item = Listing(listing_title = form.listing_title.data,
        purchase_price = form.purchase_price.data,
        description = form.description.data,
        game_condition = form.game_condition.data,
        game_release_date = form.game_release_date.data,
        game_genre = form.game_genre.data,
        game_classification = form.game_classification.data,
        game_platform = form.game_platform.data,
        listing_img_url = db_file_path,
        user_id = current_user.id)

        db.session.add(item)

        db.session.commit()
        flash('Listing created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('CreateListing.html', form = form)

# Function for confirming a bid.
@bp.route('/confirmbid', methods=['GET', 'POST'])
@login_required
def confirmbid():
    bid = Bid(date_of_bid = date.today(), user_id = current_user.id,
    listing_id = request.form['listingID'], contact_number = current_user.contact_number)
    db.session.add(bid)
    db.session.commit()
    flash('Bid submitted!', 'success')
    return redirect(url_for('main.home'))