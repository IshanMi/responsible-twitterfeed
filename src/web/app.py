from flask import Flask, render_template, request, redirect, url_for
from src.web.feed_creator import TwitterClient
from src.database import db_session
from dotenv import load_dotenv, find_dotenv
from rq import Queue
from src.database.worker import conn
from src.database.stream_job import stream_job
from src.database.restful_api import Query
from flask_restful import Api
import os


load_dotenv(find_dotenv())
app = Flask(__name__, template_folder=os.getenv("TEMPLATES_FOLDER"))
app.static_folder = os.getenv("STATIC")
app.config['DATABASE_URL'] = os.getenv("DATABASE_URL")
api = Api(app)
# app.url_map.converters["string"] = StringConverter

new_session_maker = db_session.create_session_maker(conn=app.config["DATABASE_URL"])
new_session = new_session_maker()
twitter_client = TwitterClient(factory=new_session)
q = Queue(connection=conn)


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
            # Ensure 1 <= value <= cap

            # Ensure # of tweets shown < cap
            quantity = min(int(quantity), cap)

            # Ensure # of tweets shown is >= 1
            quantity = max(1, quantity)
        except ValueError:
            quantity = cap

        return redirect(url_for('search_results', search_term=search_term, num=quantity))


@app.route('/motivation')
def motivation():
    return render_template('motivation.html')


@app.route('/search/<string:search_term>')
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
        return redirect(url_for('go_live', query_list=search_terms))


@app.route('/live/<string:query_list>', methods=["GET", "POST"])
def go_live(query_list):
    twitter_client.start_stream()

    try:
        q.enqueue(stream_job(client=twitter_client, queries=query_list))
    except AttributeError:
        pass
    api.add_resource(Query, '/db/<string:query_list>a')

    return "Database has been populated with tweets"


if __name__ == '__main__':
    app.run()
