"""
Post class for easier management
"""

import datetime
import json

from bs4 import element
from bson import json_util


class Post:
    def __init__(self, ident: int, title: str, url: str) -> None:
        self._id = ident
        self.title = title
        self.url = url
        self.created = datetime.datetime.now()

    def __str__(self) -> str:
        return f"Post #{self._id}: {self.title} [{self.url}] ({self.created})"

    def to_json(self):
        return json.dumps(self.__dict__, default=json_util.default)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_html_elem(cls, tr_elem: element.Tag):
        """
        Class method to create Posts from <tr> tag, retrieved by bs4 from https://news.ycombinator.com
        - 'title' and 'url' are stripped
        - if 'url' path is relevant, the domain is added to make the link absolute
        """

        ident: int = int(tr_elem.attrs["id"])

        last_td: element.Tag = tr_elem.findChildren("td")[-1]
        a_in_td: element.Tag = last_td.findChild("a")

        title = a_in_td.text.strip()
        url = a_in_td.attrs["href"].strip()

        if url.startswith("item?"):
            url = f"https://news.ycombinator.com/{url}"

        return cls(ident, title, url)
