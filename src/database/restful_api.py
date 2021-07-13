from flask_restful import Resource
import sqlite3


class Query(Resource):
    def get(self, query_list):
        return {}
