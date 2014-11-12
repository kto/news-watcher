# -*- coding: utf-8 -*-
import unittest
import feedparser
from mock import Mock
import time


class TestFeed():
    def __init__(self):
        self.link = None
        self.entries = [{}]


class TestNewsParser(unittest.TestCase):
    def setUp(self):
        from newsparser import newsparser
        self.np = newsparser.NewsParser()
        self.np.feedparser = Mock(feedparser)
        self.np.feedparser.parse = Mock(return_value=self.get_test_feed())

    def tearDown(self):
        if self.np:
            self.np.feed_check_scheduler.cancel()
            self.np = None

    def get_test_feed(self, link='http://test.feed'):
        test_feed = TestFeed()
        test_feed.link = link
        test_feed.entries = [{'title': 'lorem ipsum test title_keyword',
                              'content': [{'value': 'test contents, content_keyword'}],
                              'summary': 'test summary, summary_keyword',
                              'link': 'http://just.a.test.link',
                              'tags': [{'label': None,
                                        'scheme': None,
                                        'term': u'tag_keyword'}]}]
        return test_feed

    def test_import_module(self):
        try:
            import newsparser  # NOQA
        except ImportError as ie:
            self.fail('Failed to import newsparser: {0}'.format(repr(ie)))

    def test_import_class(self):
        try:
            from newsparser.newsparser import NewsParser  # NOQA
        except ImportError as ie:
            self.fail('Failed to import NewsParser class: {0}'.format(repr(ie)))  # NOQA

    def test_add_feed(self):
        self.np.add_feed('http://test.feed')
        self.assertEquals(1, len(self.np.feeds))
        self.assertTrue('http://test.feed' in self.np.feeds)

    def test_add_multiple_feeds(self):
        self.np.add_feed('http://test.feed')
        self.np.add_feed('http://another.feed')
        self.assertTrue('http://test.feed' in self.np.feeds)
        self.assertTrue('http://another.feed' in self.np.feeds)

    def test_adding_same_feed_twice(self):
        test_feed = self.get_test_feed()
        self.np.add_feed('http://test.feed')
        self.np.add_feed('http://test.feed')
        self.assertEquals(1, len(self.np.feeds))

    def test_add_feeds(self):
        test_feeds = [self.get_test_feed(), self.get_test_feed('http://another.feed')]
        self.np.add_feeds(test_feeds)
        self.assertEquals(2, len(self.np.feeds))
        self.assertEquals(test_feeds, self.np.feeds)

    def test_add_feeds_with_same_url_multiple_times(self):
        test_feeds = ['http://test.feed', 'http://test.feed']
        self.np.add_feeds(test_feeds)
        self.assertEquals(1, len(self.np.feeds))
        self.assertEquals(['http://test.feed'], self.np.feeds)

    def test_set_keywords(self):
        keywords = ['foo', 'bar', 'bah', 'baz']
        self.np.set_keywords(keywords)
        self.assertEquals(keywords, self.np.keywords)

    def test_set_empty_keywords_list(self):
        self.np.set_keywords([])
        self.assertEquals([], self.np.keywords)

    def test_set_check_interval(self):
        self.np.set_check_interval(5)
        self.assertEquals(5, self.np.check_interval)

    def test_default_check_interval(self):
        self.assertEquals(self.np.DEFAULT_CHECK_INTERVAL, self.np.check_interval)

    def test_feeds_parsed_after_added(self):
        test_feed = self.get_test_feed()
        self.np.feedparser.parse = Mock(return_value=test_feed)
        self.np.add_feed(test_feed.link)
        self.assertEquals(1, len(self.np.parsed_feeds))
        self.assertEquals(test_feed, self.np.parsed_feeds[test_feed.link])
        self.np.feedparser.parse.assert_called_with(test_feed.link)

    def test_feeds_parsed_after_interval_passed(self):
        self.np.set_check_interval(0.5/60)
        test_feed = self.get_test_feed()
        self.np.feedparser.parse = Mock(return_value=test_feed)
        self.np.add_feed(test_feed.link)
        time.sleep(1)
        self.assertEquals(2, len(self.np.feedparser.parse.call_args_list))

    def test_alert_sent_when_keywords_found_in_title(self):
        self.alert_func_called = False

        def alert_func(feed_entries):
            self.alert_func_called = True
            self.assertTrue('title_keyword' in feed_entries[0]['title'])

        test_feed = self.get_test_feed()
        self.np.set_alert_callback(alert_func)
        self.np.set_keywords(['title_keyword'])
        self.np.add_feed(test_feed.link)
        self.assertTrue(self.alert_func_called)

    def test_no_alert_sent_when_keywords_not_found(self):
        self.alert_func_called = False

        def alert_func(feed_entries):
            self.alert_func_called = True

        test_feed = self.get_test_feed()
        self.np.set_alert_callback(alert_func)
        self.np.set_keywords(['this_will_not_be_found'])
        self.np.add_feed(test_feed.link)
        self.assertFalse(self.alert_func_called)
