# Database classes.
from . import db
from datetime import datetime
from flask_login import UserMixin, LoginManager

# Defines User table/class.
class User(db.Model,UserMixin):
    __tablename__='Users'

    # Attributes.
    id = db.Column(db.Integer, primary_key=True)
    account_creation_date = db.Column(db.Date, nullable=False)
    user_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)
    contact_number = db.Column(db.String(50), nullable=False)
	# Password is never stored in the DB, an hashed password is stored.
    password_hash = db.Column(db.String(255), nullable=False)

    # Foreign keys.
    bid_userid = db.relationship('Bid', backref='userid', foreign_keys = 'Bid.user_id')
    bid_number = db.relationship('Bid', backref='number', foreign_keys = 'Bid.contact_number')
    listing = db.relationship('Listing', backref='user')

    # Returns self.
    def __repr__(self):
        return "{}".format(self.user_name)

# Defines Bid table/class.
class Bid(db.Model):
    __tablename__='Bids'

    # Attributes.
    id = db.Column(db.Integer, primary_key=True)
    date_of_bid = db.Column(db.Date, nullable=False)

    # Foreign keys.
    contact_number = db.Column(db.String(50), db.ForeignKey('Users.contact_number'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('Items.id'))

    # Returns self.
    def __repr__(self):
        return "<Name: {}, ID: {}>".format(self.date_of_bid, self.id)

# Defines Transaction table/class.
class Transaction(db.Model):
    __tablename__ = 'Purchases'

    # Attributes.
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.Date, nullable=False)

    # Foreign keys.
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('Items.id'))

    # Returns self.
    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.purchase_date, self.id)

# Defines Listing table/class.
class Listing(db.Model):
    __tablename__= 'Items'

    # Attributes.
    id = db.Column(db.Integer, primary_key=True)
    listing_title = db.Column(db.String(150), index=True)
    purchase_price = db.Column(db.String(16), nullable=False)
    date_posted = db.Column(db.Date, nullable=False, default=datetime.now())
    description = db.Column(db.String(250), nullable=False)
    availability_status = db.Column(db.String(64), nullable=False, default='Available')
    game_condition = db.Column(db.String(64), nullable=False)
    game_release_date = db.Column(db.Date, nullable=False)
    listing_img_url = db.Column(db.String(60), nullable=False, default='default.jpg')
    game_classification = db.Column(db.String(64), nullable=False)
    game_platform = db.Column(db.String(64), nullable=False)
    game_genre = db.Column(db.String(64), nullable=False)
    bid = db.relationship('Bid', backref='listing')
    transaction = db.relationship('Transaction', backref='listing')

    # Foreign keys.
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    # Returns self.
    def __repr__(self):
        return "{}".format(self.id)
