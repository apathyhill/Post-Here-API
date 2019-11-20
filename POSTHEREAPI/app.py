from decouple import config
from flask import Flask, render_template, request, redirect
from praw import Reddit
from urllib.parse import quote_plus
from .db_model import DB, User
from sqlalchemy import exists
import json


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
    print(config("DATABASE_URL"))

    DB.init_app(app)

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return "reset."


    @app.route("/post_to_reddit/<subreddit>/<title>/<article>")
    def post_to_reddit(subreddit, article, title):
        return redirect("https://www.reddit.com/r/{}/submit?text={}&title={}".format(subreddit, (article), quote_plus(title)))

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


    @app.route("/app_login_user_name", methods=["POST"])
    def app_login_user_name():
        if request.method == "POST":
            print(request.data)
        return "test"

    @app.route("/app_login_password", methods=["POST"])
    def app_login_password():
        if request.method == "POST":
            print(request.data)
        return "test"

    @app.route("/article_text", methods=["POST", "GET"])  
    def article_text():
        if request.method == "POST":
            print(request.data)
        if request.method == "GET":
            return {"text": "This is a test."}
        return "test"
        
    @app.route("/app_login_password", methods=["POST"])
    def title_of_article():
        if request.method == "POST":
            print(request.data)
        return "test"

    @app.route("/recommended_subreddits", methods=["POST"])
    def recommended_subreddits():
        if request.method == "POST":
            print(request.data)
        return "test"

    @app.route("/user_choice_subreddit", methods=["POST"]) 
    def user_choice_subreddit():
        if request.method == "POST":
            print(request.data)
        return "test"
        

    return app