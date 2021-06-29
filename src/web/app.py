from flask import Flask, render_template, request, redirect, url_for
from src.web.feed_creator import TwitterClient
from src.database import db_session
from dotenv import load_dotenv, find_dotenv
import redis
from rq import Queue
from rq.job import Job
from src.database.worker import conn

import os


load_dotenv(find_dotenv())
app = Flask(__name__, template_folder=os.getenv("TEMPLATES_FOLDER"))
app.static_folder = os.getenv("STATIC")
app.config['DB_FILE'] = os.getenv("DB_FILE")
# app.url_map.converters["string"] = StringConverter

twitter_client = TwitterClient()
new_session_maker = db_session.create_session_maker(conn=f'sqlite:///{app.config["DB_FILE"]}')
new_session = new_session_maker.begin()
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
            quantity = max(1, min(int(quantity), cap))
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

    twitter_client.start_stream(factory=new_session)
    # start_stream_job = q.enqueue(
    #     twitter_client.start_stream,
    #     kwargs={
    #         'factory_maker': new_session_maker
    #     }
    # )

    filter_stream_job = q.enqueue(
        twitter_client.stream.filter,
        kwargs={
            'track': query_list,
            'languages': ["en"]
        }
    )
    # depends_on=start_stream_job
    return "Done"


if __name__ == '__main__':
    app.run()

