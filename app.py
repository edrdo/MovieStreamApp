import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    x = db.execute('SELECT COUNT(*) AS movies FROM MOVIE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS actors FROM ACTOR').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS streams FROM STREAM').fetchone()
    stats.update(x)
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Movies
@APP.route('/movies/')
def list_movies():
    movies = db.execute(
      '''
      SELECT MovieId, Title, Year, Duration 
      FROM MOVIE
      ORDER BY Title
      ''').fetchall()
    return render_template('movie-list.html', movies=movies)


@APP.route('/movies/<int:id>/')
def get_movie(id):
  movie = db.execute(
      '''
      SELECT MovieId, Title, Year, Duration 
      FROM MOVIE 
      WHERE movieId = %s
      ''', id).fetchone()

  if movie is None:
     abort(404, 'Movie id {} does not exist.'.format(id))

  genres = db.execute(
      '''
      SELECT GenreId, Label 
      FROM MOVIE_GENRE NATURAL JOIN GENRE 
      WHERE movieId = %s 
      ORDER BY Label
      ''', id).fetchall()

  actors = db.execute(
      '''
      SELECT ActorId, Name
      FROM MOVIE_ACTOR NATURAL JOIN ACTOR
      WHERE MovieId = %s
      ORDER BY Name
      ''', id).fetchall()

  streams = db.execute(
      ''' 
      SELECT StreamId, StreamDate
      FROM STREAM
      WHERE MovieId = %s
      ORDER BY StreamDate Desc
      ''', id).fetchall();
  return render_template('movie.html', 
           movie=movie, genres=genres, actors=actors, streams=streams)

@APP.route('/movies/search/<expr>/')
def search_movie(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  movies = db.execute(
      ''' 
      SELECT MovieId, Title
      FROM MOVIE 
      WHERE Title LIKE %s
      ''', expr).fetchall()
  return render_template('movie-search.html',
           search=search,movies=movies)

# Actors
@APP.route('/actors/')
def list_actors():
    actors = db.execute('''
      SELECT ActorId, Name 
      FROM Actor
      ORDER BY Name
    ''').fetchall()
    return render_template('actor-list.html', actors=actors)


@APP.route('/actors/<int:id>/')
def view_movies_by_actor(id):
  actor = db.execute(
    '''
    SELECT ActorId, Name
    FROM ACTOR 
    WHERE ActorId = %s
    ''', id).fetchone()

  if actor is None:
     abort(404, 'Actor id {} does not exist.'.format(id))

  movies = db.execute(
    '''
    SELECT MovieId, Title
    FROM MOVIE NATURAL JOIN MOVIE_ACTOR
    WHERE ActorId = %s
    ORDER BY Title
    ''', id).fetchall()

  return render_template('actor.html', 
           actor=actor, movies=movies)
 
@APP.route('/actors/search/<expr>/')
def search_actor(expr):
  search = { 'expr': expr }
  # SQL INJECTION POSSIBLE! - avoid this!
  actors = db.execute(
      ' SELECT ActorId, Name'
      ' FROM ACTOR '
      ' WHERE Name LIKE \'%' + expr + '%\''
    ).fetchall()

  return render_template('actor-search.html', 
           search=search,actors=actors)

# Genres
@APP.route('/genres/')
def list_genres():
    genres = db.execute('''
      SELECT GenreId, Label 
      FROM GENRE
      ORDER BY Label
    ''').fetchall()
    return render_template('genre-list.html', genres=genres)

@APP.route('/genres/<int:id>/')
def view_movies_by_genre(id):
  genre = db.execute(
    '''
    SELECT GenreId, Label
    FROM GENRE 
    WHERE GenreId = %s
    ''', id).fetchone()

  if genre is None:
     abort(404, 'Genre id {} does not exist.'.format(id))

  movies = db.execute(
    '''
    SELECT MovieId, Title
    FROM MOVIE NATURAL JOIN MOVIE_GENRE
    WHERE GenreId = %s
    ORDER BY Title
    ''', id).fetchall()

  return render_template('genre.html', 
           genre=genre, movies=movies)

# Streams
@APP.route('/streams/<int:id>/')
def get_stream(id):
  stream = db.execute(
      '''
      SELECT StreamId, StreamDate, Charge, MovieId, Title, CustomerId, Name
      FROM STREAM NATURAL JOIN MOVIE NATURAL JOIN CUSTOMER 
      WHERE StreamId = %s
      ''', id).fetchone()

  if stream is None:
     abort(404, 'Stream id {} does not exist.'.format(id))

  return render_template('stream.html', stream=stream)


# Staff
@APP.route('/staff/')
def list_staff():
    staff = db.execute('''
      SELECT S1.StaffId AS StaffId, 
             S1.Name AS Name,
             S1.Job AS Job, 
             S1.Supervisor AS Supervisor,
             S2.Name AS SupervisorName
      FROM STAFF S1 LEFT JOIN STAFF S2 ON(S1.Supervisor = S2.StaffId)
      ORDER BY S1.Name
    ''').fetchall()
    return render_template('staff-list.html', staff=staff)

@APP.route('/staff/<int:id>/')
def show_staff(id):
  staff = db.execute(
    '''
    SELECT StaffId, Name, Supervisor, Job
    FROM STAFF
    WHERE staffId = %s
    ''', id).fetchone()

  if staff is None:
     abort(404, 'Staff id {} does not exist.'.format(id))
  superv={}
  if not (staff['Supervisor'] is None):
    superv = db.execute(
      '''
      SELECT Name
      FROM staff
      WHERE staffId = %s
      ''', staff['Supervisor']).fetchone()
  supervisees = []
  supervisees = db.execute(
    '''
      SELECT StaffId, Name from staff
      where Supervisor = %s
      ORDER BY Name
    ''',id).fetchall()

  return render_template('staff.html', 
           staff=staff, superv=superv, supervisees=supervisees)

