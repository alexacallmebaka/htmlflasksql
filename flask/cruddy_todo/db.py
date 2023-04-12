#this file is for managing database connections.
import sqlite3

#allow us to access the current app instance (current_app) and current session (g).
from flask import current_app, g

#get us a db connection.
def get_db():
    #don't open the connection if it's already open in the session.
    if 'db' not in g:

        #connect to the database
        #parse_decltypes just tells sqlite to convert the declared type of each column to its python type.
        #https://docs.python.org/3/library/sqlite3.html#sqlite3.PARSE_DECLTYPES
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        #this tells the session how to extract rows from the database. it will return rows that behave like dictionaries.
        g.db.row_factory = sqlite3.Row

    return g.db


#close the db connection and remove the connection from session.
def close_db(e=None):
    db = g.pop('db', None)

    #close the db connection if it exists.
    if db is not None:
        db.close()

#Tell flask to close the db when the app has finished running
def init_app(app):
    app.teardown_appcontext(close_db)
