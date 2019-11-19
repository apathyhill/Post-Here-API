from decouple import config
from flask import Flask, render_template, request, redirect
from praw import Reddit
from urllib.parse import quote_plus


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template("home.html")

    @app.route("/post_to_reddit/<subreddit>/<title>")
    def predict_subreddit(subreddit, title):
        return redirect("https://www.reddit.com/r/{}/submit?title={}".format(subreddit, title))

    return app