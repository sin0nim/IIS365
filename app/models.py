from datetime import datetime
from time import time
import jwt
from flask import current_app
# from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

'''
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
'''
    
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    user_type = db.Column(db.String(1), default='1')
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    money = db.Column(db.Float(10,2), default=0.0)
    password_hash = db.Column(db.String(128))
    about = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    house_offers = db.relationship('House', backref='lessor', lazy='dynamic')
    purchase_offers = db.relationship('Purchase', backref='seller', lazy='dynamic')
    # filters = db.relationship('Filter', backref='user', lazy='dynamic')
    '''    
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'Users', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    '''
    
    def __repr__(self):
        return f'<Username {self.username}, user_type {self.user_type }, phone: {self.phone}, e-mail: {self.email}>'
    
    def rent_offers(self):
        offered = House.query.filter_by(holder=self.id)
        return offered.order_by(House.actual_date.desc())
    
    def buy_offers(self):
        offered = Purchase.query.filter_by(owner=self.id)
        return offered.order_by(Purchase.actual_date.desc())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    '''
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    '''
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
            # .decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)
'''

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

# hs_models

class House(db.Model):
    __tablename__ = 'house'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    living_area = db.Column(db.Integer)
    kitchen_area = db.Column(db.Integer)
    nfloor = db.Column(db.Integer)
    floors = db.Column(db.Integer)
    holder = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Float(6,2))
    prepay = db.Column(db.Float(6,2))
    insurance = db.Column(db.Integer)
    rental_period = db.Column(db.Integer)
    contract_type = db.Column(db.Integer)
    client_commission = db.Column(db.Integer)
    agents = db.Column(db.Boolean)
    agents_commission = db.Column(db.Integer)
    address = db.Column(db.Text)
    metro = db.Column(db.Integer)
    metro_dist = db.Column(db.Integer)
    walk = db.Column(db.Boolean)
    railway_dist = db.Column(db.Integer)
    kitchen_furn = db.Column(db.Boolean)
    room_furn = db.Column(db.Boolean)
    refrigerator = db.Column(db.Boolean)
    tv = db.Column(db.Boolean)
    washing_automat = db.Column(db.Boolean)
    dishwasher = db.Column(db.Boolean)
    internet = db.Column(db.Boolean)
    balcony = db.Column(db.Boolean)
    windows = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    bath = db.Column(db.Boolean)
    shower_cab = db.Column(db.Boolean)
    parking = db.Column(db.Boolean)
    repair_need = db.Column(db.Integer)
    actual_date = db.Column(db.Date)

    def __str__(self):
        return f"{('комната', 'квартира', 'дом',)[self.type]}, {self.rooms} комнат, {self.nfloor} этаж, адрес: {self.address}, цена: {int(self.price)} р/{('день', 'месяц', 'год')[self.rental_period]}, дата объявления: {self.actual_date}"

'''
class Holder(db.Model):
    __tablename__ = 'holder'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(256))
    first_name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(12))
    pass_hash = db.Column(db.String(512))

    def __str__(self):
        return self.name

class Renter(db.Model):
    __tablename__ = 'renter'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(256))
    first_name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(11))
    pass_hash = db.Column(db.String(512))
    
    def __str__(self):
        return self.name
'''

# pch_models

class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    living_area = db.Column(db.Integer)
    kitchen_area = db.Column(db.Integer)
    nfloor = db.Column(db.Integer)
    floors = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Float(6,2))
    # prepay = db.Column(db.Float(6,2))
    # insurance = db.Column(db.Integer)
    # rental_period = db.Column(db.Integer)
    # contract_type = db.Column(db.Integer)
    # client_commission = db.Column(db.Integer)
    agents = db.Column(db.Boolean)
    agents_commission = db.Column(db.Integer)
    address = db.Column(db.Text)
    metro = db.Column(db.Integer)
    metro_dist = db.Column(db.Integer)
    walk = db.Column(db.Boolean)
    railway_dist = db.Column(db.Integer)
    kitchen_furn = db.Column(db.Boolean)
    room_furn = db.Column(db.Boolean)
    refrigerator = db.Column(db.Boolean)
    tv = db.Column(db.Boolean)
    washing_automat = db.Column(db.Boolean)
    dishwasher = db.Column(db.Boolean)
    internet = db.Column(db.Boolean)
    columnes = db.Column(db.Integer)
    balcony = db.Column(db.Boolean)
    windows = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    bath = db.Column(db.Boolean)
    shower_cab = db.Column(db.Boolean)
    parking = db.Column(db.Boolean)
    repair_need = db.Column(db.Integer)
    actual_date = db.Column(db.Date)

    def __str__(self):
        return f"{('комната', 'квартира', 'дом',)[self.type]}, {self.rooms} комнат, {self.nfloor} этаж, цена: {int(self.price)} р"

'''
class Owner(db.Model):
    __tablename__ = 'owner'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(256))
    first_name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(12))
    pass_hash = db.Column(db.String(512))

    def __str__(self):
        return self.name



class Buyer(db.Model):
    __tablename__ = 'buyer'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(256))
    first_name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(11))
    pass_hash = db.Column(db.String(512))
    
    def __str__(self):
        return self.name
'''