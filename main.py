from crypt import methods
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests

from forms.MovieForm import MovieForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-collection.sqlite3"
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # def __init__(self, title, year, description, rating, ranking, review, img_url) -> None:
    #     super().__init__()

    #     self.title = title
    #     self.year = year
    #     self.description = description
    #     self.ranking = ranking
    #     self.rating = rating
    #     self.review = review
    #     self.img_url = img_url


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.ranking).all()

    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    movie_form = MovieForm()
    if movie_form.validate_on_submit():
        print(movie_form.title.data)
        new_movie = Movie(
            title=movie_form.title.data,
            year=movie_form.year.data,
            description=movie_form.description.data,
            rating=movie_form.rating.data,
            ranking=movie_form.ranking.data,
            review=movie_form.review.data,
            img_url=movie_form.img_url.data
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', form=movie_form)


db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=8080)
