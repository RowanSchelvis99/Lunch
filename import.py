from flask import Flask, render_template, request
from models import *
import csv
import os
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
print(f"Database URL: {os.getenv('DATABASE_URL')}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("pseudo_data.csv")
    reader = csv.reader(f)
    next(reader)

    for restaurant_name, location, item_name, price in reader:

        restaurant = Restaurant(name = restaurant_name,location = location)
        db.session.add(restaurant)
        db.session.commit()

    # Create a new menu item and associate it with the restaurant
        menu_item = MenuItem(item_name=item_name, price=float(price))
        restaurant.menu_items.append(menu_item)

        db.session.commit()

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()