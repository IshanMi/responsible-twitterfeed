from flask import Flask, render_template, request, redirect, url_for
from src.feed_creator import get_api, get_tweets
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, template_folder=os.getenv("TEMPLATES_FOLDER"))
app.static_folder = os.getenv("STATIC")
app.config["API_KEY"] = os.getenv("API_KEY")
app.config["SECRET_KEY"] = os.getenv("API_SECRET_KEY")


@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def get_search_term():
    if request.method == "GET":
        return render_template("form.html")
    else:
        search_term = request.form["search_term"]
        quantity = request.form["quantity"]

        # Double check that it's a number
        if quantity.isdigit():
            quantity = int(quantity)

            if quantity > 100:
                quantity = 100
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


if __name__ == '__main__':
    app.run()
