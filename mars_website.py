#### BE SURE TO START MONGOD before launching this program

# Setup Dependencies
from flask import Flask, render_template
from scrape_mars import scrape_fourth_planet
import pprint
import pymongo

app = Flask(__name__)

@app.route('/')
def welcome():

    # Retrive the "Red_Planet_News" from the MongoDB
    # It's in the mars_data collection
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.MarsDB

    # There is only one document in the collection
    Red_Planet_News = db.mars_data.find_one()

    return render_template ('index.html', The_News=Red_Planet_News)

@app.route('/scrape')
def scrape():

    # Scrape the web for the latest on Mars
    # Store the results in a dictionary called "Red_Planet_News"
    Red_Planet_News = scrape_fourth_planet()

    # Store the results in a MongoDB called MarsDB, in a collection called "mars_data"
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define the 'MarsDB' database in Mongo
    db = client.MarsDB

    # Drop the "mars_data" collection if it exists
    db.mars_data.drop()

    # Add the "mars_info" dictionary to the "mars_data" collection
    db.mars_data.insert_one (Red_Planet_News)

    # Finished
    return render_template ('index.html', The_News=Red_Planet_News)

if __name__ == "__main__":
    app.run(debug=True)