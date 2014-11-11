import unittest

class TestNewsWatch(unittest.TestCase):
	def test_import(self):
		try:
			import news_watch
		except ImportError as ie:
			self.fail('Failed to import news_watch: {0}'.format(repr(ie)))

