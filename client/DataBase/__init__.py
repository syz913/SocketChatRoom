import sqlite3

def run():
       conn = sqlite3.connect("pydb.db")

       # create user table
       conn.execute('''CREATE TABLE users
              (username  TEXT  PRIMARY KEY   NOT NULL,
              password   TEXT  NOT NULL);''')
       # create message table
       conn.execute('''CREATE TABLE messages
              (username  TEXT  PRIMARY KEY  NOT NULL,
              date  TEXT  NOT NULL,
              message   TEXT  NOT NULL);''')

       conn.close()
