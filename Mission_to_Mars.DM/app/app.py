from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import Scrape_Mars 

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection to mars_app db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars_data=mars_data) 

# Scrape_Mars python script is a module bc we are importing it; 
# .scrape was a function in the other script, now a method here.
@app.route("/scrape")
def scraper():
    mars_collection = mongo.db.mars_collection
    scraped_data = Scrape_Mars.scrape()
    
# upsert=True...if nothing exists, it is inserted, or it is updated
    mars_collection.update({}, scraped_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
