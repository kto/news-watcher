import unittest


class TestNewsParser(unittest.TestCase):
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
