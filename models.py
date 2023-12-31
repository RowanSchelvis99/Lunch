from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Create database
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    reviews = db.relationship("Review", backref="author", lazy=True)
    

    def is_active(self):
        return True

    # Generate a unique password hash for password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password against hashed version
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable =False)
    restaurant_id= db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="reviews")

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    menu_items = db.relationship("MenuItem", backref="restaurant", lazy=True)
    reviews = db.relationship("Review", backref="restaurant", lazy=True)

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)

