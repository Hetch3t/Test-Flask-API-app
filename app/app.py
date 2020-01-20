from threading import Thread

from flask import Flask, jsonify, request
from pymongo import ASCENDING, MongoClient
from classes.Timer import IntervalTimer

app = Flask(__name__)

@app.route("/posts")
def index():
    try:
        offset: int = request.args.get("offset", default=0, type=int)
        limit: int = request.args.get("limit", default=5, type=int)
        order: str = request.args.get("order", default="_id", type=str)

    except:
        return "Error in parameters."

    docs = list(mongo_collection.find().sort(order).skip(offset).limit(limit))

    return jsonify(docs)

def init_db(host="localhost"):
    mongo_client = MongoClient(host, port=27017)
    mongo_db = mongo_client.db
    return mongo_db.posts


if __name__ == "__main__":
    mongo_collection = init_db('mongo_db')
    thread = Thread(target=IntervalTimer.start_scanning, args=[mongo_collection])
    thread.start()

    app.run(port=3000, host="0.0.0.0")
