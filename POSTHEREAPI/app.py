from decouple import config
from flask import Flask, render_template, request, redirect
from praw import Reddit
from urllib.parse import quote_plus


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template("home.html")

    @app.route("/post_to_reddit/<subreddit>/<article>")
    def predict_subreddit(subreddit, article):
        return redirect("https://www.reddit.com/r/{}/submit?text=".format(subreddit, article))

    return app