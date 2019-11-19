from decouple import config
from flask import Flask, render_template, request
from praw import Reddit
from urllib.parse import quote_plus

REDDIT = Reddit(client_id=config("CLIENT_ID"),
                     client_secret=config("CLIENT_SECRET"),
                     user_agent=config("USER_AGENT"))

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return render_template("home.html")


    @app.route("/predict", methods=["POST"])
    def predict_subreddit():
        if request.method == "POST":
            title = request.values["title"]
            # predictions = process_title(title)
            predictions = [{"name": "me_irl", "confidence": 100 }]
            return render_template("predictions.html", predictions=predictions, title=title, title_url=quote_plus(title))
        return "ERROR"
    return app