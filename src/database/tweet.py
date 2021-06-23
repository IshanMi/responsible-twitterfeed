import sqlalchemy
from src.database.modelbase import SQLAlchemyBase


class Tweet(SQLAlchemyBase):

    __tablename__ = "Tweet-Database"

    text = sqlalchemy.Column(sqlalchemy.String)  # text
    time = sqlalchemy.Column(sqlalchemy.DateTime)  # created_at
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)  # id
    id_str = sqlalchemy.Column(sqlalchemy.String)  #id_str

    def __repr__(self):
        return f'Tweet w/ID#{id}'


"""
All keys belonging to a Tweet:

dict_keys(['created_at', 'id', 'id_str', 'text', 'source', 
'truncated', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 
'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 
'user', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 
'extended_tweet', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', 
'entities', 'favorited', 'retweeted', 'possibly_sensitive', 'filter_level', 'lang', 
'timestamp_ms'])

"""