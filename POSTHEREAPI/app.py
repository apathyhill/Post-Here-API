from decouple import config
from flask import Flask, render_template, request, redirect
from praw import Reddit
from urllib.parse import quote_plus
from urllib.request import urlopen
from .db_model import DB, User
from sqlalchemy import exists
import json
import pickle
import requests


def create_app():
    app = Flask(__name__)

    pickle_url = "https://github.com/apathyhill/Post-Here-API/blob/heroku/pickle/model-{:02d}.pkl?raw=true"
    pickle_text = b""
    for i in range(0, 34):
        print(i)
        pickle_text += requests.get(url.format(i)).content

    model = pickle.loads(pickle_text)

    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
    print(config("DATABASE_URL"))

    DB.init_app(app)

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return "reset."


    @app.route("/post_to_reddit", methods=["POST"])
    def post_to_reddit():
        if request.method == "POST":
            data = json.loads(request.data) # {"article": "", "title": "", "subreddit": ""}
            new_url = "https://www.reddit.com/r/{}/submit?text={}&title={}".format(data["subreddit"], 
                                                                                         quote_plus(data["article"]), 
                                                                                      quote_plus(data["title"]))
            print(new_url)
            return redirect(new_url)

    @app.route("/register", methods=["POST"])
    def register():
        if request.method == "POST":
            data = json.loads(request.data)
            if DB.session.query(exists().where(User.username==data["username"])).scalar():
                return "User already exists!"
            else:
                db_user = User(username=data["username"], password=data["password"])
                DB.session.add(db_user)
                DB.session.commit()
                return "Made a user!"
        return "ERROR"

    @app.route("/login", methods=["POST"])
    def login():
        if request.method == "POST":
            data = json.loads(request.data)
            if DB.session.query(exists().where(User.username==data["username"])).scalar():
                db_user = User.query.filter(User.username == data["username"]).one()
                if db_user.password == data["password"]:
                    return "Logged in as {}!".format(db_user.username)
        return "Could not login..."

    @app.route("/predict", methods=["POST"])
    def login():
        if request.method == "POST":
            data = json.loads(request.data)
            pred = model.predict(data["article"])[0]
            print(pred)
            return {"prediction": pred}
        return "ERROR"

        

    return app