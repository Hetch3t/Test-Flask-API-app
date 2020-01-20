import json
from datetime import datetime

import pytest
from bs4 import BeautifulSoup

from app.classes.Post import Post


def test_initialization():
    post = Post(123, 'TestTitle', 'http://google.com')

    assert post._id == 123
    assert post.title == 'TestTitle'
    assert post.url == 'http://google.com'
    assert type(post.created) == datetime


def test_convert_to_string():
    post = Post(123, 'TestTitle', 'http://google.com')

    assert str(post).startswith("Post #123: TestTitle [http://google.com]")


def test_convert_to_dict():
    post = Post(123, 'TestTitle', 'http://google.com')
    post_dict = post.to_dict()

    assert post_dict['_id'] == 123
    assert post_dict['title'] == 'TestTitle'
    assert post_dict['url'] == 'http://google.com'


def test_init_from_tr():
    tr_text = '<tr class="athing" id="22098832"><td align="right" valign="top" class="title"><span class="rank">4.</span></td><td valign="top" class="votelinks"><center><a id="up_22098832" href="vote?id=22098832&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><a href="https://www.sqlite.org/howtocorrupt.html" class="storylink">How to Corrupt an SQLite Database File</a><span class="sitebit comhead"> (<a href="from?site=sqlite.org"><span class="sitestr">sqlite.org</span></a>)</span></td></tr>'
    soup = BeautifulSoup(tr_text, features="html.parser")
    tr = soup.find('tr')

    post = Post.from_html_elem(tr)

    assert post._id == 22098832
    assert post.url == 'https://www.sqlite.org/howtocorrupt.html'
    assert post.title == 'How to Corrupt an SQLite Database File'