import time
import traceback
from typing import List

import requests
from bs4 import BeautifulSoup, element
from pymongo.collection import Collection

from .Post import Post


class HackerNewsCrawler:
    def __init__(self, mongo_collection: Collection):
        self.m_coll = mongo_collection

    def _retrieve_page(self) -> str:
        """
        Getting page content
        """

        return requests.get("https://news.ycombinator.com").text

    def _parse_page(self) -> List[Post]:
        """
        Parsing page with BeautifulSoup. Making array of Posts
        """

        soup: BeautifulSoup
        rows: List[element.Tag]
        posts: List[Post] = []

        soup = BeautifulSoup(self._retrieve_page(), features="html.parser")
        rows = soup.find_all("tr", {"class": "athing"})
        for row in rows:
            posts.append(Post.from_html_elem(row))
        return posts

    def _save_posts(self, posts: List[Post]) -> None:
        """
        Saving posts to MongoDB to 'posts' collection
        """

        for post in posts:
            self.m_coll.update_one(
                {"_id": post._id}, {"$setOnInsert": post.to_dict()}, upsert=True
            )

    def scan(self):
        """
        Main class function. Consists of two parts - page getter+parser and DB saver.
        Both parts are put into try/except blocks for app stability purposes (no crashes).
        """

        try:
            posts = self._parse_page()
        except:
            print("> Error during retrieving or parsing page.")
            traceback.print_exc()

        try:
            self._save_posts(posts)
        except:
            print("> Error during saving posts to DB.")
            traceback.print_exc()


