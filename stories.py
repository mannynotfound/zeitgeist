#!/usr/bin/env python3
import os
import json
import io
import argparse
import feedparser
import firebase
from json_utils import load_json, dump_json
from time import mktime

def parse_item(item):
    parsed = {
            'headline': item.get('title'),
            'summary': item.get('summary'),
            'published': item.get('published'),
            'media': item.get('media_content'),
            'link': item.get('link')
            }

    # add unix timestamp if parsed time available
    published_parsed = item.get('published_parsed')
    if published_parsed:
        parsed['unix_timestamp'] = mktime(published_parsed)

    return parsed

def extract_results(parsed_feed, **opts):
    stories = []
    source = opts.get('source')

    print('PARSING >>> {0}'.format(source))
    print('')
    for item in parsed_feed.get('entries'):
        parsed_item = parse_item(item)
        parsed_item['source'] = source
        print(parsed_item['headline'])
        print(parsed_item.get('unix_timestamp'))
        stories.append(parsed_item)

    print('')
    print('~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')
    print('')
    return stories

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--firebase', help = 'save data to firebase', action="store_true")
    args = vars(ap.parse_args())

    path = os.path.dirname(os.path.realpath(__file__))
    models_path = path + '/models'
    dump_path = path + '/dump/stories'
    newsfeeds = load_json(models_path, 'feeds')

    for feed in newsfeeds:
        parsed_feed = feedparser.parse(feed['feed'])
        results = extract_results(parsed_feed, **feed)
        if args['firebase']:
            fb = firebase.create_firebase()
            db = fb.database().child('stories').child(feed['source']).set(results)
        else:
            dump_json(dump_path, feed['source'], results)
