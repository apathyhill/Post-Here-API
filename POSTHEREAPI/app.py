from decouple import config
from flask import Flask, render_template, request, redirect
from praw import Reddit
from urllib.parse import quote_plus
from urllib.request import urlopen
from .db_model import DB, User
from sqlalchemy import exists, and_
import json
import pickle
import requests
import os
import string
import random


def create_app():
    app = Flask(__name__)

    f = open("nlp_model.pkl", "rb")
    model = pickle.load(f)
    f.close()

    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
    print(config("DATABASE_URL"))

    DB.init_app(app)

    def get_current_user(session_key):
        if DB.session.query(exists().where(User.session_key==session_key)).scalar():
            return User.query.filter(User.session_key == session_key).one()
        return None

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return "reset."


    @app.route("/post_to_reddit", methods=["POST"])
    def post_to_reddit():
        if request.method == "POST":
            data = json.loads(request.data) # {"article": "", "title": "", "subreddit": ""}
            user = get_current_user(request.headers["authorization"])
            if user:
                pred = model.predict([data["article"]])[0]
                new_url = "https://www.reddit.com/r/{}/submit?text={}&title={}".format(data["subreddit"], 
                                                                                         quote_plus(data["article"]), 
                                                                                      quote_plus(data["title"]))
                print(new_url)
                return redirect(new_url)
            else:
                return "Not logged in!"

    @app.route("/register", methods=["POST"])
    def register():
        if request.method == "POST":
            data = json.loads(request.data)
            print(data)
            if DB.session.query(exists().where(User.username==data["username"])).scalar():
                return "User already exists!"
            else:
                db_user = User(username=data["username"], password=data["password"])
                db_user.session_key = "".join(random.sample(string.ascii_letters, 32))
                DB.session.add(db_user)
                DB.session.commit()
                print(db_user.session_key)
                return {"session_key": db_user.session_key }
        return {}

    @app.route("/login", methods=["POST"])
    def login():
        if request.method == "POST":
            try:
                data = json.loads(request.data)
                db_user = User.query.filter(and_(User.username == data["username"], User.password == data["password"])).one()
                db_user.session_key = "".join(random.sample(string.ascii_letters, 32))
                print(db_user.session_key)
                DB.session.commit()
                return db_user.session_key
            except Exception as e:
                pass
        return "Could not login..."

    @app.route("/predict", methods=["POST"])
    def predict():
        if request.method == "POST":
            data = json.loads(request.data)
            print(data)
            user = get_current_user(request.headers["authorization"])
            if user:
                pred = model.predict([data["article"]])[0]
                print(pred)
                return {"prediction": pred}
            else:
                return "Not logged in!"
        return "ERROR"    

    return app