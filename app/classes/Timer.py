
from pymongo.collection import Collection
import time
from .Crawler import HackerNewsCrawler


class IntervalTimer:
    @staticmethod
    def start_scanning(m_coll, interval=1200):
        """
        Scanning thread entrypoint. Default scanning interval is 30m (1800s)
        """

        crawler = HackerNewsCrawler(m_coll)
        while True:
            crawler.scan()
            time.sleep(interval)


