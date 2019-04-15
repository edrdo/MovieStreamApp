from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.db import get_db

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    db = get_db()
    stats = dict()
    x = db.execute('SELECT COUNT(*) AS movies FROM MOVIE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS actors FROM ACTOR').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS streams FROM STREAM').fetchone()
    stats.update(x)
    return render_template('index.html',stats=stats)
