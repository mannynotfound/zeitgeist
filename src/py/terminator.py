#!/usr/bin/env python3
import argparse
import twitter_search

ap = argparse.ArgumentParser()
ap.add_argument('-t', '--term', help = 'term to search for')
args = vars(ap.parse_args())

term = args['term']

twitter_search_page = twitter_search.TwitterPager().get_iterator(term)

count = 0
for page in twitter_search_page:
    for tweet in page['tweets']:
        print("{0} id: {1} text: {2}".format(count, tweet['id_str'], tweet['text']))
        count += 1
