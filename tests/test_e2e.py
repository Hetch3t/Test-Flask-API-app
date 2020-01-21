import os
import tempfile

import pytest

from app import app
from setup import init_db, init_timer, manual_scan
from classes import IntervalTimer

@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_collection_name = "test_posts"
    init_db(app, coll=test_collection_name)

    # Initial database clear
    app.config['COLLECTION'].delete_many({})

    with app.test_client() as test_client:
        yield test_client

def teardown_module():
    # Clearing database (removing collection) after tests
    app.config['COLLECTION'].drop()


def test_no_index_endpoint(client):
    rv = client.get('/')
    assert 404 == rv.status_code


def test_json_returned(client):
    rv = client.get('/posts')
    assert rv.is_json == True


def test_empty_json(client):
    rv = client.get('/posts')
    assert rv.json == []

def test_posts_endpoint(client):
    manual_scan(app)

    rv = client.get('/posts')

    assert 200 == rv.status_code
    assert len(rv.json) == 5

    rv = client.get('/posts?limit=30')
    assert len(rv.json) == 30

    rv = client.get('/posts?offset=25&limit=30')
    assert len(rv.json) == 5

    rv = client.get('/posts?offset=20&limit=7')
    assert len(rv.json) == 7

    # Checking sort by _id
    rv = client.get('/posts?limit=16&order=_id&order_direction=asc')
    data = rv.json
    assert data[0]['_id'] < data[1]['_id']
    assert data[0]['_id'] < data[15]['_id']

    rv = client.get('/posts?limit=16&order=_id&order_direction=desc')
    data = rv.json
    assert data[0]['_id'] > data[1]['_id']
    assert data[0]['_id'] > data[15]['_id']

    # Checking sort by title
    rv = client.get('/posts?limit=16&order=title&order_direction=asc')
    data = rv.json
    assert data[0]['title'] < data[1]['title']
    assert data[0]['title'] < data[15]['title']

    rv = client.get('/posts?limit=16&order=title&order_direction=desc')
    data = rv.json
    assert data[0]['title'] > data[1]['title']
    assert data[0]['title'] > data[15]['title']

    # Checking sort by created
    rv = client.get('/posts?limit=16&order=created&order_direction=asc')
    data = rv.json
    assert data[0]['created'] <= data[1]['created']
    assert data[0]['created'] <= data[15]['created']

    rv = client.get('/posts?limit=16&order=created&order_direction=desc')
    data = rv.json
    assert data[0]['created'] >= data[1]['created']
    assert data[0]['created'] >= data[15]['created']