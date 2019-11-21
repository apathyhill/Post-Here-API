"""This is my database models"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    username = DB.Column(DB.Text(), nullable=False, primary_key=True)
    password = DB.Column(DB.Text(), nullable=False)
    session_key = DB.Column(DB.Text())
