import os
from flask_login import LoginManager

from flask import Flask, session, render_template, request,redirect
from flask import render_template, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import current_user, login_required
from forms import ReviewForm
from models import Review
from flask_login import LoginManager
from flask_login import login_user
from sqlalchemy import func


from models import *

app = Flask(__name__, static_url_path='/static')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'BDca8199'
Session(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET"])
def restaurant_list():
    # Get a list of all restaurants from the database
    restaurants = Restaurant.query.all()

    average_ratings = {}
    for restaurant in restaurants:
        average_rating = (
            db.session.query(func.round(func.avg(Review.rating), 1))
            .filter_by(restaurant_id=restaurant.id)
            .scalar()
        )
        average_ratings[restaurant.id] = average_rating

    return render_template("restaurants.html", restaurants=restaurants, average_rating=average_ratings)

@app.route("/restaurant/<int:restaurant_id>/reviews", methods=["GET"])
def restaurant_reviews(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        reviews = Review.query.filter_by(restaurant_id=restaurant.id).all()

        # Calculate average rating
        average_rating = (
            db.session.query(func.round(func.avg(Review.rating), 1))
            .filter_by(restaurant_id=restaurant.id)
            .scalar()
        )

        return render_template(
            "restaurant_reviews.html",
            restaurant=restaurant,
            reviews=reviews,
            average_rating=average_rating,
        )
    else:
        return render_template("error.html", message="Restaurant not found"), 404

@app.route("/restaurant/<int:restaurant_id>", methods=["GET"])
def restaurant_menu(restaurant_id):
    restaurant_info = {
        1: {
            "image": "/static/restaurants/1.jpg",
            "description": "Café-restaurant Polder bevindt zich op het terrein van Science Park Amsterdam, precies tussen de kennisinstituten. Je kunt dit gezellige restaurant de hele dag door bezoeken: van roerei bij het ontbijt tot een broodje voor de lunch en een uitgebreid diner (veel biologisch!) in de avonden. Om op te warmen, kun je plaatsnemen in een van de fauteuils rond de houtkachel. Bij mooi weer is er ook een leuk terras met picknicktafels.",
            "opening_hours": {
                "Monday": "9:00 - 0:00",
                "Tuesday": "9:00 - 0:00",
                "Wednesday": "9:00 - 0:00",
                "Thursday": "9:00 - 0:00",
                "Friday": "9:00 - 0:00",
                "Saturday": "9:00 - 0:00",
                "Sunday": "9:00 - 0:00",
            },
        },
        2: {
            "image": "/static/restaurants/2.jpg",
            "description": "Description for Restaurant 2",
            "opening_hours": {
                "Monday": "9:00 AM - 7:00 PM",
                "Tuesday": "9:00 AM - 7:00 PM",
                "Wednesday": "10:00 AM - 5:00 PM",
                "Thursday": "9:00 AM - 7:00 PM",
                "Friday": "9:00 AM - 9:00 PM",
                "Saturday": "11:00 AM - 9:00 PM",
                "Sunday": "11:00 AM - 7:00 PM",
            },
        },
        3: {
            "image": "/static/restaurants/3.jpg",
            "description": "Description for Restaurant 3",
            "opening_hours": {
                "Monday": "8:00 AM - 6:00 PM",
                "Tuesday": "8:00 AM - 6:00 PM",
                "Wednesday": "9:00 AM - 4:00 PM",
                "Thursday": "8:00 AM - 6:00 PM",
                "Friday": "8:00 AM - 8:00 PM",
                "Saturday": "10:00 AM - 8:00 PM",
                "Sunday": "10:00 AM - 6:00 PM",
            },
        },
        4: {
            "image": "/static/restaurants/4.jpg",
            "description": "Description for Restaurant 4",
            "opening_hours": {
                "Monday": "7:00 AM - 5:00 PM",
                "Tuesday": "7:00 AM - 5:00 PM",
                "Wednesday": "8:00 AM - 3:00 PM",
                "Thursday": "7:00 AM - 5:00 PM",
                "Friday": "7:00 AM - 7:00 PM",
                "Saturday": "9:00 AM - 7:00 PM",
                "Sunday": "9:00 AM - 5:00 PM",
            },
        },
        5: {
            "image": "/static/restaurants/5.jpg",
            "description": "Description for Restaurant 5",
            "opening_hours": {
                "Monday": "6:00 AM - 4:00 PM",
                "Tuesday": "6:00 AM - 4:00 PM",
                "Wednesday": "7:00 AM - 2:00 PM",
                "Thursday": "6:00 AM - 4:00 PM",
                "Friday": "6:00 AM - 6:00 PM",
                "Saturday": "8:00 AM - 6:00 PM",
                "Sunday": "8:00 AM - 4:00 PM",
            },
        },
        6: {
            "image": "/static/restaurants/6.jpg",
            "description": "Description for Restaurant 6",
            "opening_hours": {
                "Monday": "5:00 AM - 3:00 PM",
                "Tuesday": "5:00 AM - 3:00 PM",
                "Wednesday": "6:00 AM - 1:00 PM",
                "Thursday": "5:00 AM - 3:00 PM",
                "Friday": "5:00 AM - 5:00 PM",
                "Saturday": "7:00 AM - 5:00 PM",
                "Sunday": "7:00 AM - 3:00 PM",
            },
        },
        7: {
            "image": "/static/restaurants/7.jpg",
            "description": "Description for Restaurant 7",
            "opening_hours": {
                "Monday": "4:00 AM - 2:00 PM",
                "Tuesday": "4:00 AM - 2:00 PM",
                "Wednesday": "5:00 AM - 12:00 PM",
                "Thursday": "4:00 AM - 2:00 PM",
                "Friday": "4:00 AM - 4:00 PM",
                "Saturday": "6:00 AM - 4:00 PM",
                "Sunday": "6:00 AM - 2:00 PM",
            },
        },
    }

    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
        print("Debug: Menu Items:", menu_items)

        info = restaurant_info.get(restaurant_id, {})

        return render_template(
            "restaurant_menu.html",
            restaurant=restaurant,
            menu_items=menu_items,
            info=info,
        )
    else:
        return render_template("error.html", message="Restaurant not found"), 404


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Make sure username is submitted
        if not request.form.get("username"):
            return render_template("error.html", message="No username subitted"), 404
        
        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        # Make sure the username is not already taken
        if user:
            return render_template("error.html", message = "Username is taken"), 404

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Make sure passwords is not filled in blank
        if not password or not confirmation:
            return render_template("error.html", message = "Must provide password"), 404
        
        if password != confirmation:
            return render_template("error.html", message = "Password must match"), 404
        
        # Make a unique hash for the password

        new_user = User(username=request.form.get("username"))
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Return user to home page
        return redirect("/")
    
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must provide username", "error")
            return render_template("login.html")
        
        elif not request.form.get("password"):
            flash("Must provide password", "error")
            return render_template("login.html")

 
        user = User.query.filter_by(username=request.form.get("username")).first()

        if not user or not user.check_password(request.form.get("password")):
            flash("Invalid username or password", "error")
            return render_template("login.html")


        login_user(user)

        flash(f"Logged in as {user.username}", "success")

        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for("restaurant_list"))

    else:
        return render_template("login.html")
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()

    return redirect("/")


@app.route("/write_review/<int:restaurant_id>", methods=["GET", "POST"])
@login_required
def write_review(restaurant_id):
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            content=form.content.data,
            rating=form.rating.data,
            user_id=current_user.id,
            restaurant_id=restaurant_id
        )
        db.session.add(review)
        db.session.commit()
        flash("Review submitted successfully!", "success")

        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for("restaurant", restaurant_id=restaurant_id))

    return render_template("write_review.html", form=form)

@app.route("/restaurant/<int:restaurant_id>")
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template("restaurant.html", restaurant=restaurant, reviews=reviews)

@app.route("/test")
def test():
    return render_template("test.html")
