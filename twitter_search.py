#!/usr/bin/env python3
import json
import sys
import os
import io
import argparse
import TwitterWebsiteSearch
import firebase
import json_utils


class TwitterSearch():
    def __init__(self, term, opts):
        self.dump_path = os.path.dirname(os.path.realpath(__file__)) + '/dump'
        self.term = term
        self.limit = opts['limit']
        self.use_firebase = opts['firebase']
        self.print_count = 0
        self.total_count = 0
        self.all_tweets = []
        self.check_existing()
        self.do_twitter_search()

    def check_existing(self):
        if self.use_firebase:
            fb = firebase.create_firebase()
            db_tweets = fb.database().child('tweets').child(self.term).get().val()
            if db_tweets:
                self.all_tweets = db_tweets
                self.print_count = len(db_tweets)

        else:
            if not os.path.exists(self.dump_path):
                os.makedirs(self.dump_path)
            else:
                try:
                    current_json = json_utils.load_json(self.dump_path, self.term)
                    if len(current_json) > 0:
                        self.all_tweets = current_json
                        self.print_count = len(current_json)
                except Exception as e:
                    json_utils.dump_json(self.dump_path, self.term, [])


    def save_to_firebase(self):
        fb = firebase.create_firebase()
        db = fb.database().child('tweets').child(self.term.replace('#', '')).set(self.all_tweets[0:10000])


    def save_data(self):
        if self.use_firebase:
            self.save_to_firebase()
        else:
            json_utils.dump_json(self.dump_path, self.term, self.all_tweets)


    def do_twitter_search(self):
        twitter_search_page = TwitterWebsiteSearch.TwitterPager().get_iterator(self.term)
        for page in twitter_search_page:
            for tweet in page['tweets']:
                self.total_count += 1
                if self.limit and self.total_count >= self.limit:
                    print('EXITING!')
                    sys.exit(1)
                elif len([e for e in self.all_tweets if e['id_str'] == tweet['id_str']]) == 0:
                    self.print_count += 1
                    print("{0} | {1}".format(self.print_count, tweet['text']))
                    self.all_tweets.append(tweet)
                    if len(self.all_tweets) % 100 == 0:
                        self.all_tweets = json_utils.sort_by_time(self.all_tweets)
                        self.save_data()


if __name__ == '__main__':
    # parse cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--term', help = 'term to search for')
    ap.add_argument('-l', '--limit', type=int, help = 'max amount of tweets to search for', nargs='?', default=0)
    ap.add_argument('-f', '--firebase', help = 'save data to firebase', action="store_true")

    args = vars(ap.parse_args())
    term = args['term'].replace('"', '').replace('#', '')

    TwitterSearch(term, {
            'limit': args['limit'],
            'firebase': args['firebase']
            })
