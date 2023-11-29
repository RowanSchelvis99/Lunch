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

    # Dictionary to keep track of restaurant objects by name
    restaurants_dict = {}

    for restaurant_name, location, item_name, price in reader:
        # Check if the restaurant already exists in the dictionary
        if restaurant_name not in restaurants_dict:
            # If not, create a new restaurant object and add it to the database
            restaurant = Restaurant(name=restaurant_name, location=location)
            db.session.add(restaurant)
            db.session.commit()
            
            # Add the restaurant to the dictionary for future reference
            restaurants_dict[restaurant_name] = restaurant

            print(f"Added restaurant: {restaurant_name} at {location}")
        else:
            # If the restaurant already exists, retrieve it from the dictionary
            restaurant = restaurants_dict[restaurant_name]

        # Create a new menu item and associate it with the restaurant
        menu_item = MenuItem(item_name=item_name, price=float(price), restaurant_id=restaurant.id)
        db.session.add(menu_item)
        print(f"Added menu item: {item_name} for {restaurant_name} (ID: {menu_item.id})")

    db.session.commit()

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()
if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()