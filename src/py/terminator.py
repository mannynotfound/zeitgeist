#!/usr/bin/env python3
import json
import sys
import os
import io
import argparse
import twitter_search

# parse cli arguments
ap = argparse.ArgumentParser()
ap.add_argument('-t', '--term', help = 'term to search for')
ap.add_argument('-l', '--limit', help = 'max amount of tweets to search for')

args = vars(ap.parse_args())
term = args['term']

if args['limit'] != None:
    limit = int(args['limit'])
else:
    limit = False

# track our state
total_count = 0
print_count = 0
all_tweets = []

# create / load the directory
def load_json(path, filename):
    with io.open('{0}/{1}.json'.format(path, filename),
                 encoding='utf-8') as f:
        return json.loads(f.read())

def dump_json(path, term, data):
    with open(path + '/' + term + '.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f)

dump_path = os.path.dirname(os.path.realpath(__file__)) + '/dump'
if not os.path.exists(dump_path):
    os.makedirs(dump_path)
else:
    try:
        current_json = load_json(dump_path, term)
        if len(current_json) > 0:
            all_tweets = current_json
            print_count = len(current_json)

    except Exception as e:
        print('EXCEPTION LOADING JSON', e)
        dump_json(dump_path, term, [])

# iterate through results
twitter_search_page = twitter_search.TwitterPager().get_iterator(term)
for page in twitter_search_page:
    for tweet in page['tweets']:
        total_count += 1
        if limit and total_count >= limit:
            print('EXITING!')
            sys.exit()
        else:
            added = False
            for existing in all_tweets:
                if (existing['id_str'] == tweet['id_str']):
                    added = True
            if not added:
                print_count += 1
                print("{0} | {1}".format(print_count, tweet['text']))
                all_tweets.append(tweet)
                if len(all_tweets) % 100 == 0:
                    try:
                        dump_json(dump_path, term, all_tweets)
                    except:
                        print('ERROR DUMPIN JSON')

