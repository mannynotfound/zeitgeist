#!/usr/bin/env python3
import json
import os
import io
import argparse
import twitter_search

# parse cli arguments
ap = argparse.ArgumentParser()
ap.add_argument('-t', '--term', help = 'term to search for')
args = vars(ap.parse_args())
term = args['term']

# track our state
count = 0
all_tweets = []

# create / load the directory
def load_json(path, filename):
    with io.open('{0}/{1}.json'.format(path, filename),
                 encoding='utf-8') as f:
        return json.loads(f.read())

def dump_json(path, term, data):
    with open(path + '/' + term + '.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f)

dump_path = os.path.dirname(os.path.realpath(__file__)) + '/term'
if not os.path.exists(dump_path):
    os.makedirs(dump_path)
else:
    try:
        current_json = load_json(dump_path, term)
        if len(current_json) > 0:
            all_tweets = current_json

    except Exception as e:
        print('EXCEPTION LOADING JSON', e)
        dump_json(dump_path, term, [])

# iterate through results
twitter_search_page = twitter_search.TwitterPager().get_iterator(term)
for page in twitter_search_page:
    for tweet in page['tweets']:
        added = False
        for existing in all_tweets:
            if (existing['id_str'] == tweet['id_str']):
                print('ALREADY ADDED TWEET')
                added = True
        if not added:
            all_tweets.append(tweet)
            if len(all_tweets) % 100 == 0:
                dump_json(dump_path, term, all_tweets)

        count += 1
        print("{0} id: {1} text: {2}".format(count, tweet['id_str'], tweet['text']))
