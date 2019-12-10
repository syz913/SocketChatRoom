import sqlite3
import time

def run():
       conn = sqlite3.connect("socketdb.db")

       # create user table
       conn.execute('''CREATE TABLE users
              (username  TEXT  PRIMARY KEY   NOT NULL,
              password   TEXT  NOT NULL);''')
       # create message table
       conn.execute('''CREATE TABLE messages
              (username  TEXT  NOT NULL,
              date  TEXT  NOT NULL,
              message   TEXT  NOT NULL,
              type   TEXT  NOT NULL);''')

       conn.close()

def save_message(username, date, message, type):
       conn = sqlite3.connect("socketdb.db")
       c = conn.cursor()
       c.execute("insert into messages (username, date, message, type) values (?, ?, ?, ?)",
              (username, date, message, type))
       conn.commit()
       conn.close()