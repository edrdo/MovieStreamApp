import pymysql

import os
from flask import g


def executor(self,sql,args=None):
  print('=== Access to DB ===')
  print('SQL: ' + sql)
  print('Args: ' + str(args))
  self.cursor.execute(sql, args)
  return self.cursor

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = pymysql.connect(host=os.environ['DB_HOST'], 
                               user=os.environ['DB_USER'], 
                               password=os.environ['DB_PASS'],
                               db=os.environ['DB_SCHEMA'],
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        g.db.cursor = g.db.cursor()
        pymysql.connections.Connection.execute = executor;
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.cursor.close()
        db.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
