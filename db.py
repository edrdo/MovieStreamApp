import logging
import pymysql
import re


# Change this if necessary
CONFIG = {
  'DB': 'movie_stream',
  'USER': 'guest',
  'PASSWORD': 'guest',
  'HOST': '127.0.0.1',
  'PORT': 3306,
  'CHARSET': 'utf8'
}

global DB
DB = None

def connect():
  global DB
  c = pymysql.connect(db=CONFIG['DB'],
                       user=CONFIG['USER'], 
                       password=CONFIG['PASSWORD'],
                       host=CONFIG['HOST'], 
                       port=CONFIG['PORT'],
                       charset=CONFIG['CHARSET'],
                       cursorclass=pymysql.cursors.DictCursor)
  c._cursor_ = c.cursor()
  DB = c
  logging.info('Connected to database %s' % CONFIG['DB'])

def execute(sql,args=None):
  global DB
  sql = re.sub('\s+',' ', sql)
  logging.info('SQL: {} Args: {}'.format(sql,args))
  DB._cursor_.execute(sql, args)
  return DB._cursor_

def close():
  global DB
  DB._cursor_.close()
  DB.close()

