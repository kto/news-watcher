import feedparser
import time
from threading import Timer


class NewsParser():
    DEFAULT_CHECK_INTERVAL = 10

    def __init__(self):
        self.feeds = []
        self.keywords = []
        self.check_interval = self.DEFAULT_CHECK_INTERVAL
        self.feedparser = feedparser
        self.parsed_feeds = {}
        self.feed_check_scheduler = Timer(self.check_interval * 60, self.update_feeds, ())
        self.feed_check_scheduler.start()
        self.alert_callback = None

    def set_alert_callback(self, alert_callback):
        self.alert_callback = alert_callback

    def check_keywords(self, feed):
        send_alert = False
        for entry in feed.entries:
            if send_alert:
                break
            for keyword in self.keywords:
                if keyword in entry['summary'] or keyword in entry['title']:
                    send_alert = True
                    break
                for content in entry['content']:
                    if keyword in content['value']:
                        send_alert = True
                        break
                for tag in entry['tags']:
                    if keyword in tag['term']:
                        send_alert = True
                        break
        if send_alert:
            self.alert_callback(feed)

    def parse_feed(self, feed):
        parsed_feed = self.feedparser.parse(feed)
        self.check_keywords(parsed_feed)
        return parsed_feed

    def add_feed(self, feed):
        if feed not in self.feeds:
            self.feeds.append(feed)
            self.parsed_feeds.update({feed: self.parse_feed(feed)})

    def add_feeds(self, feeds):
        for feed in feeds:
            self.add_feed(feed)

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_check_interval(self, interval):
        self.feed_check_scheduler.cancel()
        self.check_interval = interval
        self.feed_check_scheduler = Timer(self.check_interval * 60, self.update_feeds, ())
        self.feed_check_scheduler.start()

    def update_feeds(self):
        if self.feeds:
            parsed_feeds = {}
            for feed in self.feeds:
                parsed_feeds.update({feed: self.feedparser.parse(feed)})
            self.parsed_feeds = parsed_feeds
            self.feed_check_scheduler = Timer(self.check_interval * 60, self.update_feeds, ())
            self.feed_check_scheduler.start()
