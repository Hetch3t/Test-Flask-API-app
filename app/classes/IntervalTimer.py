
from pymongo.collection import Collection
import time
from .HackerNewsCrawler import HackerNewsCrawler


class IntervalTimer:
    @staticmethod
    def start_scanning(m_coll, interval, repeated):
        """
        Scanning thread entrypoint. Default scanning interval is 30m (1800s)
        """

        crawler = HackerNewsCrawler(m_coll)

        if repeated:
            while True:
                crawler.scan()
                time.sleep(interval)
        else:
            crawler.scan()


