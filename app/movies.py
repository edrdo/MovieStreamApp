from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('movies', __name__)

@bp.route('/movies')
def index():
    """Show all the movies."""
    movies = get_db().execute(
        ' SELECT MovieId, Title, Year, Duration FROM MOVIE'
        ' ORDER BY MovieId'
    ).fetchall()
    return render_template('movie-list.html', movies=movies)


@bp.route('/movies/<int:id>', methods=('GET', 'POST'))
def get_movie(id):
  db = get_db()
  movie = db.execute(
      ' SELECT MovieId, Title, Year, Duration'
      ' FROM MOVIE WHERE movieId = %s', 
      id
    ).fetchone()

  if movie is None:
     abort(404, "Movie id {0} doesn't exist.".format(id))

  genres = db.execute(
    ' SELECT Label'
    ' FROM MOVIE_GENRE NATURAL JOIN GENRE'
    ' WHERE movieId = %s'
    ' ORDER BY Label', 
    id
  ).fetchall()

  actors = db.execute(
    ' SELECT ActorId, Name'
    ' FROM MOVIE_ACTOR NATURAL JOIN ACTOR'
    ' WHERE MovieId = %s'
    ' ORDER BY Name', 
    id
  ).fetchall()

  streams = db.execute(
    ' SELECT StreamId, StreamDate '
    ' FROM STREAM'
    ' WHERE MovieId = %s'
    ' ORDER BY StreamDate Desc',
    id
  ).fetchall();
  return render_template('movie.html', 
           movie=movie, genres=genres, actors=actors, streams=streams)


@bp.route('/movies/search/<expr>', methods=('GET', 'POST'))
def search_actor(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%';
  movies = get_db().execute(
      ' SELECT MovieId, Title'
      ' FROM MOVIE WHERE Title LIKE %s',
      expr
    ).fetchall()

  return render_template('movie-search.html',
           search=search,movies=movies)
