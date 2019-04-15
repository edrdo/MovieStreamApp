from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('streams', __name__)

@bp.route('/streams/<int:id>', methods=('GET', 'POST'))
def get_stream(id):
  stream = get_db().execute(
      ' SELECT StreamId, StreamDate, Charge, MovieId, Title, CustomerId, Name'
      ' FROM STREAM NATURAL JOIN MOVIE NATURAL JOIN CUSTOMER WHERE StreamId = %s', 
      id
    ).fetchone()

  if stream is None:
     abort(404, "Stream id {0} doesn't exist.".format(id))

  return render_template('stream.html', stream=stream)
