# Functions for displaying search results.
from flask import Blueprint, render_template, request
from .models import Listing
from . import db
from sqlalchemy import desc


# Create a blueprint.
bp = Blueprint('result', __name__, url_prefix='/results')


# Route for sorting by game condition.
@bp.route('/condition_id=<game_condition>')
def condition(game_condition):
    listings = Listing.query \
    .filter_by(game_condition=game_condition) \
    .order_by(desc(Listing.id)).all()
    search_category = request.args.get('search_category')
    print(search_category)
    return render_template('result.html', listings=listings, search_category = search_category)

# Route for sorting by game classification.
@bp.route('/classification_id=<game_classification>')
def classification(game_classification):
    listings = Listing.query \
    .filter_by(game_classification=game_classification) \
    .order_by(desc(Listing.id)).all()
    search_category = request.args.get('search_category')
    return render_template('result.html', listings=listings, search_category = search_category)

# Route for sorting by game platform.
@bp.route('/platform_id=<game_platform>')
def platform(game_platform):
    listings = Listing.query \
    .filter_by(game_platform=game_platform) \
    .order_by(desc(Listing.id)).all()
    search_category = request.args.get('search_category')
    return render_template('result.html', listings=listings, search_category = search_category)

# Route for sorting by game genre.
@bp.route('/genre_id=<game_genre>')
def genre(game_genre):
    listings = Listing.query \
    .filter_by(game_genre=game_genre) \
    .order_by(desc(Listing.id)).all()
    search_category = request.args.get('search_category')
    return render_template('result.html', listings=listings, search_category = search_category)

