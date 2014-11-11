class NewsParser():
    def __init__(self):
        self.feeds = []

    def add_feed(self, feed):
        if feed not in self.feeds:
            self.feeds.append(feed)

    def get_feeds(self):
        return self.feeds
