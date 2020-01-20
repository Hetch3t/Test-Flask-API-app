import json

import pytest
import pymongo

from app.classes.Crawler import HackerNewsCrawler
from app.classes.Post import Post

def test_crawler():
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client.db
    coll = db.posts
    crawler: HackerNewsCrawler = HackerNewsCrawler(coll)

    assert crawler.m_coll == coll
    assert type(crawler._retrieve_page()) == str
    assert type(crawler._parse_page()) == list
    assert type(crawler._parse_page()[0]) == Post