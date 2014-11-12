# -*- coding: utf-8 -*-
import feedparser
from threading import Timer


class NewsParser():
    DEFAULT_CHECK_INTERVAL = 10

    def __init__(self, feeds=None, keywords=None, check_interval=None, alert_callback=None):
        self.keywords = keywords or []
        self.feedparser = feedparser
        self.parsed_feeds = {}
        self.alert_callback = alert_callback
        self.feeds = []
        self.feed_check_scheduler = None
        self.sent_alerts = []
        if feeds:
            self.add_feeds(feeds)
        self.set_check_interval(check_interval or self.DEFAULT_CHECK_INTERVAL)

    def set_alert_callback(self, alert_callback):
        self.alert_callback = alert_callback

    def parse_entry_for_alert(self, entry, content=None):
        entry_key = u'{0}-{1}'.format(entry['title'], entry['link'])
        if entry_key not in self.sent_alerts:
            entry_summary = ''
            entry_content = ''
            if 'summary' in entry:
                entry_summary = entry['summary']

            if content:
                entry_content = content
            elif 'content' in entry:
                entry_content = entry['content'][0]['value']

            return ({'title': entry['title'],
                           'link': entry['link'],
                           'summary': entry_summary,
                           'content': entry_content})
            self.sent_alerts.append(entry_key)

    def check_keywords(self, feed):
        alerts = []

        for entry in feed.entries:
            for keyword in self.keywords:
                if 'summary' in entry and keyword in entry['summary']:
                    alerts.append(self.parse_entry_for_alert(entry))
                    break
                if keyword in entry['title']:
                    alerts.append(self.parse_entry_for_alert(entry))
                    break
                if 'content' in entry:
                    for content in entry['content']:
                        if keyword in content['value']:
                            alerts.append(self.parse_entry_for_alert(entry, content=content['value']))
                            break
                if 'tags' in entry:
                    for tag in entry['tags']:
                        if keyword in tag['term']:
                            alerts.append(self.parse_entry_for_alert(entry))
                            break

        if alerts:
            self.alert_callback(alerts)

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
        if self.feed_check_scheduler:
            self.feed_check_scheduler.cancel()
        self.check_interval = interval
        self.feed_check_scheduler = Timer(self.check_interval * 60, self.update_feeds, ())
        self.feed_check_scheduler.start()

    def update_feeds(self):
        if self.feeds:
            parsed_feeds = {}
            for feed in self.feeds:
                parsed_feeds.update({feed: self.parse_feed(feed)})
            self.parsed_feeds = parsed_feeds
            self.feed_check_scheduler = Timer(self.check_interval * 60, self.update_feeds, ())
            self.feed_check_scheduler.start()
