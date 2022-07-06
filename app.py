# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from schemas import movie_schema, movies_schema
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movie_with_genre_and_director = db.session.query(
            Movie.id,
            Movie.title,
            Movie.description,
            Movie.trailer,
            Movie.year,
            Movie.rating,
            Genre.name.label('genre'),
            Director.name.label('director')
        ).join(Genre).join(Director)

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id:
            movie_with_genre_and_director = movie_with_genre_and_director.filter(Movie.director_id == director_id)
        if genre_id:
            movie_with_genre_and_director = movie_with_genre_and_director.filter(Movie.genre_id == genre_id)

        all_movies = movie_with_genre_and_director.all()

        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):
    def get(self, movie_id):
        try:
            movie = db.session.query(
                Movie.id,
                Movie.title,
                Movie.description,
                Movie.trailer,
                Movie.year,
                Movie.rating,
                Genre.name.label('genre'),
                Director.name.label('director')
            ).join(Genre).join(Director).filter(Movie.id == movie_id).one()
        except Exception as e:
            return str(e), 404
        return movie_schema.dump(movie), 200

    def put(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
        except Exception as e:
            return str(e), 404
        req_json = request.json

        movie.title = req_json['title']
        movie.description = req_json['description']
        movie.trailer = req_json['trailer']
        movie.year = req_json['year']
        movie.rating = req_json['rating']
        movie.genre_id = req_json['genre_id']
        movie.director_id = req_json['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()
        return "", 204

    def patch(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
        except Exception as e:
            return str(e), 404
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json['title']
        if "description" in req_json:
            movie.description = req_json['description']
        if "trailer" in req_json:
            movie.trailer = req_json['trailer']
        if "year" in req_json:
            movie.year = req_json['year']
        if "rating" in req_json:
            movie.rating = req_json['rating']
        if "genre_id" in req_json:
            movie.genre_id = req_json['genre_id']
        if "director_id" in req_json:
            movie.director_id = req_json['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()
        return "", 204

    def delete(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
        except Exception as e:
            return str(e), 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:director_id>')
class DirectorView(Resource):
    def put(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
        except Exception as e:
            return str(e), 404
        req_json = request.json

        director.name = req_json['name']

        db.session.add(director)
        db.session.commit()
        db.session.close()
        return "", 204

    def patch(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
        except Exception as e:
            return str(e), 404
        req_json = request.json

        if "name" in req_json:
            director.name = req_json['name']

        db.session.add(director)
        db.session.commit()
        db.session.close()
        return "", 204

    def delete(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
        except Exception as e:
            return str(e), 404
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genre_ns.route('/')
class GenresView(Resource):
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    def put(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
        except Exception as e:
            return str(e), 404
        req_json = request.json

        genre.name = req_json['name']

        db.session.add(genre)
        db.session.commit()
        db.session.close()
        return "", 204

    def patch(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
        except Exception as e:
            return str(e), 404
        req_json = request.json

        if "name" in req_json:
            genre.name = req_json['name']

        db.session.add(genre)
        db.session.commit()
        db.session.close()
        return "", 204

    def delete(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
        except Exception as e:
            return str(e), 404
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
