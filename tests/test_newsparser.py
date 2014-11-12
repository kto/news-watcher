import unittest
import feedparser
from mock import Mock


class TestNewsParser(unittest.TestCase):
    def get_newsparser(self):
        from newsparser import newsparser
        np = newsparser.NewsParser()
        np.feedparser = Mock(feedparser)
        return np

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

    def test_add_feed_to_watch(self):
        np = self.get_newsparser()
        np.add_feed('http://test.feed')
        self.assertEquals(1, len(np.feeds))
        self.assertTrue('http://test.feed' in np.feeds)

    def test_add_multiple_feeds(self):
        np = self.get_newsparser()
        np.add_feed('http://test.feed')
        np.add_feed('http://another.feed')
        self.assertTrue('http://test.feed' in np.feeds)
        self.assertTrue('http://another.feed' in np.feeds)

    def test_adding_same_feed_twice(self):
        np = self.get_newsparser()
        np.add_feed('http://test.feed')
        np.add_feed('http://test.feed')
        self.assertEquals(1, len(np.feeds))

    def test_add_feeds(self):
        np = self.get_newsparser()
        test_feeds = ['http://test.feed', 'http://another.feed']
        np.add_feeds(test_feeds)
        self.assertEquals(2, len(np.feeds))
        self.assertEquals(test_feeds, np.feeds)

    def test_add_feeds_with_same_feed_multiple_times(self):
        np = self.get_newsparser()
        test_feeds = ['http://test.feed', 'http://test.feed']
        np.add_feeds(test_feeds)
        self.assertEquals(1, len(np.feeds))
        self.assertEquals(['http://test.feed'], np.feeds)

    def test_set_keywords(self):
        np = self.get_newsparser()
        keywords = ['foo', 'bar', 'bah', 'baz']
        np.set_keywords(keywords)
        self.assertEquals(keywords, np.keywords)

    def test_set_empty_keywords_list(self):
        np = self.get_newsparser()
        np.set_keywords([])
        self.assertEquals([], np.keywords)

    def test_set_check_interval(self):
        np = self.get_newsparser()
        np.set_check_interval(5)
        self.assertEquals(5, np.check_interval)

    def test_default_check_interval(self):
        np = self.get_newsparser()
        self.assertEquals(np.DEFAULT_CHECK_INTERVAL, np.check_interval)

    def test_feeds_parsed_after_added(self):
        np = self.get_newsparser()
        test_feed = {'link': 'http://test.feed'}
        np.feedparser.parse = Mock(return_value=test_feed)
        np.add_feed(test_feed['link'])
        self.assertEquals(1, len(np.parsed_feeds))
        self.assertEquals(test_feed, np.parsed_feeds[test_feed['link']])
        np.feedparser.parse.assert_called_with(test_feed['link'])
