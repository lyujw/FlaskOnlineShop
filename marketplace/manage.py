# Function for managing listings.
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required
from .models import Listing, Bid, User, Transaction
from . import db
from datetime import datetime, date


# Create a blueprint.
bp = Blueprint('manage', __name__, url_prefix='/manage')

# Route for managing listings.
@bp.route('/<id>', methods=['GET', 'POST'])
@login_required
def manage(id):
    listing = Listing.query.filter_by(id=id).first_or_404()

    # For bid display.
    bids = Bid.query.filter_by(listing_id=id).join(User, Bid.user_id==User.id).\
    add_columns(User.id, User.user_name, Bid.listing_id, Bid.contact_number,
    Bid.date_of_bid, User.email_id).all()

    # For purchase display.
    purchase = Transaction.query.filter_by(listing_id=id).join(User,
    Transaction.user_id==User.id).add_columns(User.id, User.user_name,
    Transaction.id, Transaction.purchase_date, User.email_id).first()

    # Gets data from URL to post to database.
    if request.args.get('user_id') is not None and request.args.get('listing_id') is not None:
        selected = Transaction(purchase_date = date.today(), user_id = request.args.get('user_id'), listing_id = request.args.get('listing_id'))
        db.session.add(selected)
        db.session.commit()

    # Marks listing as sold on URL change.
    sold = Listing.query.filter_by(id=request.args.get('listing_id')).first()
    if sold is not None:
        sold.availability_status = 'Sold'
        db.session.commit()
        flash('Listing marked as sold!', 'success')
        return redirect(url_for('main.home'))

    return render_template('ManageListing.html', listing=listing, bids=bids, purchase=purchase, sold=sold)
