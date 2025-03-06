from flask import Flask, render_template, request, redirect
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup (SQLite for storing reviews)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# OMDB API Key
API_KEY = "ba41583f"  

# Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    review_text = db.Column(db.Text, nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Home Route (Search Movie & Show Reviews)
@app.route("/", methods=["GET", "POST"])
def index():
    movie_data = None
    reviews = []
    if request.method == "POST":
        movie_name = request.form["movie_name"]
        response = requests.get(f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}")
        movie_data = response.json()

        # Fetch reviews from database
        reviews = Review.query.filter_by(movie_title=movie_data["Title"]).all()
    
    return render_template("index.html", movie_data=movie_data, reviews=reviews)

# Route to Submit Review
@app.route("/add_review", methods=["POST"])
def add_review():
    movie_title = request.form["movie_title"]
    user_name = request.form["user_name"]
    review_text = request.form["review_text"]

    new_review = Review(movie_title=movie_title, user_name=user_name, review_text=review_text)
    db.session.add(new_review)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
