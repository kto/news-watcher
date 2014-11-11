import unittest


class TestNewsParser(unittest.TestCase):
    def get_newsparser(self):
        from newsparser import newsparser
        return newsparser.NewsParser()

    def test_import_module(self):
        try:
            import newsparser  # NOQA
        except ImportError as ie:
            self.fail('Failed to import newsparser: {0}'.format(repr(ie)))

    def test_import_class(self):
        try:
            from newsparser.newsparser import NewsParser  # NOQA
        except ImportError as ie:
            self.fail('Failed to import NewsParser class: {0}'.format(repr(ie)))

    def test_add_feed_to_watch(self):
        np = self.get_newsparser()
        np.add_feed('http://test.feed')
        self.assertTrue('http://test.feed' in np.get_feeds())
        self.assertEquals(1, len(np.get_feeds()))

    def test_add_multiple_feeds(self):
        np = self.get_newsparser()
        np.add_feed('http://test.feed')
        np.add_feed('http://another.feed')
        self.assertTrue('http://test.feed' in np.get_feeds())
        self.assertTrue('http://another.feed' in np.get_feeds())

    def test_adding_same_feed_twice(self):
        np = self.get_newsparser()
        np.add_feed('http://test.feed')
        np.add_feed('http://test.feed')
        self.assertEquals(1, len(np.get_feeds()))
