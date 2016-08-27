#!/usr/bin/env python3
import os
import io
import argparse
import feedparser
import firebase
import json_utils
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
        stories.append(parsed_item)

    sorted_stories = json_utils.sort_by_time(stories)
    print('')
    print('~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')
    print('')


    return sorted_stories

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--firebase', help = 'save data to firebase', action="store_true")
    args = vars(ap.parse_args())

    path = os.path.dirname(os.path.realpath(__file__))
    models_path = path + '/models'
    dump_path = path + '/dump/stories'
    newsfeeds = json_utils.load_json(models_path, 'feeds')

    for feed in newsfeeds:
        parsed_feed = feedparser.parse(feed['feed'])
        results = extract_results(parsed_feed, **feed)
        if args['firebase']:
            fb = firebase.create_firebase()
            db = fb.database().child('stories').child(feed['source']).set(results)
        else:
            json_utils.dump_json(dump_path, feed['source'], results)
