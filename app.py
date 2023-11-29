import os

from flask import Flask, session, render_template, request,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/", methods=["GET"])
def restaurant_list():
    # Get a list of all restaurants from the database
    restaurants = Restaurant.query.all()
    return render_template("restaurants.html", restaurants=restaurants)

@app.route("/restaurant/<int:restaurant_id>", methods=["GET"])
def restaurant_menu(restaurant_id):
    # Get the details of the selected restaurant
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        # Get the menu items for the selected restaurant
        menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
        return render_template("restaurant_menu.html", restaurant=restaurant, menu_items=menu_items)
    else:
        # Handle the case where the restaurant is not found
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

        # Request password from user
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

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message = "Must provide username"), 404

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message = "Must provide password"), 404

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if not user or not user.check_password(request.form.get("password")):
            return render_template("error.html", message = "Must provide password"), 404

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")