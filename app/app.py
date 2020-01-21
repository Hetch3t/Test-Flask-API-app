import pymongo
from flask import Flask, jsonify, request

from setup import app_factory, init_db, init_timer


app = app_factory()


@app.route("/posts")
def index():
    try:
        offset: int = request.args.get("offset", default=0, type=int)
        limit: int = request.args.get("limit", default=5, type=int)
        order: str = request.args.get("order", default="_id", type=str)
        order_direction_str: str = request.args.get(
            "order_direction", default="asc", type=str
        )

        if order_direction_str == "desc":
            order_direction = pymongo.DESCENDING
        else:
            # default behaviour
            order_direction = pymongo.ASCENDING
    except:
        return "Error in parameters.", 400

    try:
        docs = list(
            app.config["COLLECTION"]
            .find()
            .sort([(order, order_direction)])
            .skip(offset)
            .limit(limit)
        )
        return jsonify(docs)
    except:
        return "Error during reading from database.", 400


if __name__ == "__main__":
    init_db(app, host="mongo_db")
    init_timer(app)

    app.run(port=3000, host="0.0.0.0")
