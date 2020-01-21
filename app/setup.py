from threading import Thread

from flask import Flask
from pymongo import MongoClient

from classes.IntervalTimer import IntervalTimer


def app_factory():
    """
    Flask App creation Factory method
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "somesecret"

    return app


def init_db(app, host="localhost", port=27017, db="db", coll="posts"):
    """
    Initializing app collection path
    """

    mongo_client = MongoClient(host, port=port)
    mongo_db = mongo_client[db]

    app.config["COLLECTION"] = mongo_db[coll]


def init_timer(app, interval=1800):
    """
    Initializing overtime crawler
    """

    thread = Thread(
        target=IntervalTimer.start_scanning, args=[app.config["COLLECTION"], interval, True]
    )
    thread.start()

def manual_scan(app):
    IntervalTimer.start_scanning(app.config["COLLECTION"], repeated=False)