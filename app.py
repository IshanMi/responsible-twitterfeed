from flask import Flask, render_template, request, redirect, url_for
from src.feed_creator import get_api, get_tweets, start_stream
from src.url_converter import StringConverter
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__, template_folder=os.getenv("TEMPLATES_FOLDER"))
app.static_folder = os.getenv("STATIC")
app.config["API_KEY"] = os.getenv("API_KEY")
app.config["SECRET_KEY"] = os.getenv("API_SECRET_KEY")
app.url_map.converters["string"] = StringConverter


@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def get_search_term(cap = 100):
    if request.method == "GET":
        return render_template("static_form.html")
    else:
        # Could add commas for more keywords
        search_term = request.form["search_term"]
        quantity = request.form["quantity"]

        # Double check that it's a number
        if quantity.isdigit():
            quantity = int(quantity)

            if quantity > cap:
                quantity = cap
        else:
            quantity = 10

        return redirect(url_for('search_results', search_term=search_term, num=quantity))


@app.route('/search/<string:search_term>/<int:num>')
def search_results(search_term, num: int = 20):
    """ This returns a static result, not a stream. """

    # Authenticate and get the Twitter API
    twitter_api = get_api(api_key=app.config["API_KEY"], secret_key=app.config["SECRET_KEY"])

    # Get Tweets based on their search term
    sample_tweets = get_tweets(api=twitter_api, query=search_term, limit=num)
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
    print("Starting")
    # Disconnect all previous streams
    for s in streams:
        s.disconnect()

    print("Authenticating")
    # Authenticate & get the API
    twitter_api = get_api(api_key=app.config["API_KEY"], secret_key=app.config["SECRET_KEY"])

    print("Authenticated, creating new stream")
    # Get Tweets as they pour in
    new_stream = start_stream(api=twitter_api)
    streams.append(new_stream)

    print("Added new stream, filtering")
    new_stream.filter(track=query_list, languages=["en"])
    print("Done")
    return new_stream


if __name__ == '__main__':
    app.run()
