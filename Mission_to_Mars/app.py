from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pprint

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Drop old data when starting up app
mongo.db.mars.drop()

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()

    # If database/collection is empty run basic html shell
    # Otherwise, return full html with collection data
    if mars != None:
        return render_template('index.html',mars=mars)
    return render_template('empty.html')

@app.route('/scrape')
def scraper():
    mars = mongo.db.mars
    mars_scrape = scrape_mars.scrape()
    print(mars_scrape)
    mars.replace_one({}, mars_scrape, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
