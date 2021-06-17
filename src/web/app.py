from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from src.web.feed_creator import TwitterClient
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
app = Flask(__name__, template_folder=os.getenv("TEMPLATES_FOLDER"))
app.static_folder = os.getenv("STATIC")
# app.url_map.converters["string"] = StringConverter
twitter_client = TwitterClient()


@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def get_search_term(cap=100):
    if request.method == "GET":
        return render_template("static_form.html")
    else:
        # Could add commas for more keywords
        search_term = request.form["search_term"]
        quantity = request.form["quantity"]

        # Double check that it's a number
        try:
            quantity = min(int(quantity), cap)
        except ValueError:
            quantity = cap

        return redirect(url_for('search_results', search_term=search_term, num=quantity))


@app.route('/search/<string:search_term>/<int:num>')
def search_results(search_term, num: int = 20):
    """ This returns a static result, not a stream. """

    # Get Tweets based on their search term
    sample_tweets = twitter_client.get_tweets(query=search_term, limit=num)
    return render_template("search_results.html", tweets=sample_tweets)


@app.route('/stream', methods=['GET', 'POST'])
def stream():
    if request.method == "GET":
        return render_template("stream_form.html")
    else:
        search_terms = request.form.getlist("search_terms")[0].split(",")
        print(search_terms)
        return redirect(url_for('go_live', query_list=search_terms))


# Global variable to keep track of all the streams
streams = []


@app.route('/live/<string:query_list>', methods=["GET", "POST"])
def go_live(query_list):
    twitter_client.start_stream()

    twitter_client.stream.filter(track=query_list, languages=["en"])
    return "Done"


if __name__ == '__main__':
    app.run()
