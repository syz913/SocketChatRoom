import sqlite3
import time

def run():
       conn = sqlite3.connect("socketdb.db")

       # create user table
       conn.execute('''CREATE TABLE users
              (username  TEXT  PRIMARY KEY   NOT NULL,
              public_key  TEXT  NOT NULL,
              signature   TEXT  NOT NULL);''')
       # create message table
       conn.execute('''CREATE TABLE messages
              (owner  TEXT  NOT NULL,
              username  TEXT  NOT NULL,
              date  TEXT  NOT NULL,
              message   TEXT  NOT NULL,
              type   TEXT  NOT NULL);''')

       conn.close()

def save_message(owner, username, date, message, type):
       conn = sqlite3.connect("socketdb.db")
       c = conn.cursor()
       c.execute("insert into messages (owner, username, date, message, type) values (?, ?, ?, ?, ?)",
              (owner, username, date, message, type))
       conn.commit()
       conn.close()