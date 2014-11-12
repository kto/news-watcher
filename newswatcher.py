# -*- coding: utf-8 -*-
import argparse
from newsparser import newsparser


def alert_callback(feed_entries):
    for entry in feed_entries:
        print entry['title']
        print entry['link']
        print entry['summary']
        print entry['content']
        print '-----------------------------------------'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--feeds', dest='feeds', required=True,
                        help='Feed urls to parse')
    parser.add_argument('--keywords', dest='keywords', required=True,
                        help='Keywords to look for from the feeds')
    parser.add_argument('--interval', type=int, dest='interval', required=False,
                        help='Interval (in minutes) how often to update feed (default: 10 minutes)')

    args = parser.parse_args()
    np = newsparser.NewsParser(feeds=args.feeds.split(','),
                               keywords=args.keywords.split(','),
                               check_interval=args.interval,
                               alert_callback=alert_callback)

if __name__ == "__main__":
    main()
