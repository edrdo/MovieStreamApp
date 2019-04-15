from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('actors', __name__)

@bp.route('/actors')
def index():
    """Show all the actors."""
    db = get_db()
    actors = db.execute(
        ' SELECT ActorId, Name FROM Actor'
        ' ORDER BY Name'
    ).fetchall()
    return render_template('actor-list.html', actors=actors)


@bp.route('/actors/<int:id>', methods=('GET', 'POST'))
def view_movies_by_actor(id):
  db = get_db()
  actor = db.execute(
      ' SELECT ActorId, Name'
      ' FROM ACTOR WHERE actorId = %s',
      id
    ).fetchone()

  if actor is None:
     abort(404, "Actor id {0} doesn't exist.".format(id))

  movies = db.execute(
    ' SELECT MovieId, Title'
    ' FROM MOVIE NATURAL JOIN MOVIE_ACTOR'
    ' WHERE actorId = %s'
    ' ORDER BY Title', 
    id
  ).fetchall()

  return render_template('actor.html', 
           actor=actor, movies=movies)
 
@bp.route('/actors/search/<expr>', methods=('GET', 'POST'))
def search_actor(expr):
  search = { 'expr': expr }
  actors = get_db().execute(
      ' SELECT ActorId, Name'
      ' FROM ACTOR WHERE NAME LIKE \'%' + expr + '%\''
    ).fetchall()

  return render_template('actor-search.html', 
           search=search,actors=actors)

