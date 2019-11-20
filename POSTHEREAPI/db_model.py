"""This is my database models"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    username = DB.Column(DB.Text(), nullable=False)
    password = DB.Column(DB.Text(), nullable=False)
