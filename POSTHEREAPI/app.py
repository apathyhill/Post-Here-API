from decouple import config
from flask import Flask, render_template, request, redirect
from praw import Reddit
from urllib.parse import quote_plus


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template("home.html")

    @app.route("/post_to_reddit", methods=["POST"])
    def predict_subreddit():
        if request.method == "POST":
            title = request.values["title"]
            subreddit = request.values["subreddit"]
            return redirect("https://www.reddit.com/r/{}/submit?title={}".format(subreddit, quote_plus(title)))

    return app