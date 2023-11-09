import logging
import sqlite3
import re


global DB
DB = dict()

def connect():
  global DB
  c = sqlite3.connect('movie_stream.db', check_same_thread=False)
  c.row_factory = sqlite3.Row
  # lambda cursor,row:  \
  #   { col[0]: row[idx] for idx,col in enumerate(cursor.description) }
  DB['conn'] = c
  DB['cursor'] = c.cursor()
  logging.info('Connected to database')

def execute(sql,args=None):
  global DB
  sql = re.sub('\s+',' ', sql)
  logging.info('SQL: {} Args: {}'.format(sql,args))
  return DB['cursor'].execute(sql, args) \
      if args != None else DB['cursor'].execute(sql)

def close():
  global DB
  DB['conn'].close()

