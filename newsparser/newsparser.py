import feedparser


class NewsParser():
    DEFAULT_CHECK_INTERVAL = 10

    def __init__(self):
        self.feeds = []
        self.keywords = []
        self.check_interval = self.DEFAULT_CHECK_INTERVAL
        self.feedparser = feedparser
        self.parsed_feeds = {}

    def add_feed(self, feed):
        if feed not in self.feeds:
            self.feeds.append(feed)
            self.parsed_feeds.update({feed: self.feedparser.parse(feed)})

    def add_feeds(self, feeds):
        for feed in feeds:
            self.add_feed(feed)

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_check_interval(self, interval):
        self.check_interval = interval
