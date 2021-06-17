from flask import Flask, render_template
from src.feed_creator import get_api, get_tweets
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, template_folder=os.getenv("TEMPLATES_FOLDER"))
app.static_folder = os.getenv("STATIC")
app.config["API_KEY"] = os.getenv("API_KEY")
app.config["SECRET_KEY"] = os.getenv("API_SECRET_KEY")


@app.route('/')
@app.route('/home')
def feed():
    twitter_api = get_api(api_key=app.config["API_KEY"], secret_key=app.config["SECRET_KEY"])
    sample_tweets = get_tweets(api=twitter_api, query="PyBites")
    return render_template("test_api.html", tweets=sample_tweets)


if __name__ == '__main__':
    app.run()
