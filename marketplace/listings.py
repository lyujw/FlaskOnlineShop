# Function for viewing listings.
from flask import Blueprint, render_template, abort
from flask_login import current_user
from .models import Listing, Bid, User, Transaction
from . import db


# Create a blueprint.
bp = Blueprint('listings', __name__, url_prefix='/listings')

# Route for viewing listings.
@bp.route('/<id>')
def show(id):
    listing = Listing.query.filter_by(id=id).first_or_404()
    bids = Bid.query.filter_by(listing_id=id, user_id=current_user.get_id()).first()
    return render_template('ViewListing.html', listing=listing, bids = bids)
