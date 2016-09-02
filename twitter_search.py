#!/usr/bin/env python3
import os, io, re, argparse, threading
from subprocess import call
import TwitterWebsiteSearch
import firebase
import json_utils

class TwitterSearch():
    def __init__(self, term, opts):
        self.path = opts['path']
        self.dump_path = opts['path'] + '/dump/tweets'
        self.term = term
        self.use_firebase = opts['firebase']
        self.silent = opts['silent']
        self.print_count = 0
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
        db = fb.database().child('tweets').child(self.term.replace('#', '')).set(self.all_tweets)

    def save_data(self):
        if self.use_firebase:
            self.save_to_firebase()
        else:
            json_utils.dump_json(self.dump_path, self.term, self.all_tweets)

    def do_twitter_search(self):
        twitter_search_page = TwitterWebsiteSearch.TwitterPager(title=self.term).get_iterator(self.term)
        for page in twitter_search_page:
            for tweet in page['tweets']:
                if len([e for e in self.all_tweets if e['id_str'] == tweet['id_str']]) == 0:
                    self.print_count += 1
                    message = "{0} | {1}".format(self.print_count, tweet['text'])
                    if not self.silent:
                        print(message)

                    realpath = self.path + '/.master.log'
                    with open(realpath, "a") as master_log:
                        master_log.write('{0} >>> {1} {2}'.format(self.term, message, '\n'))

                    self.all_tweets.append(tweet)
                    if len(self.all_tweets) % 100 == 0:
                        self.all_tweets = json_utils.sort_by_time(self.all_tweets)
                        self.all_tweets = self.all_tweets[:10000]
                        self.save_data()

if __name__ == '__main__':
    # parse cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--terms', help = 'term(s) to search for')
    ap.add_argument('-f', '--firebase', help = 'save data to firebase', action="store_true")
    ap.add_argument('-s', '--silent', help = 'doesnt output statuses', action="store_true")
    ap.add_argument('-c', '--clear', help = 'clear inactive trends', action="store_true")

    args = vars(ap.parse_args())
    terms = list(map(lambda x: re.sub(r'(#|")', '', x).strip(), args['terms'].split(',')))

    opts = {
            'firebase': args['firebase'],
            'silent': args['silent'],
            'path': os.path.dirname(os.path.realpath(__file__))
            }

    if args['clear']:
        try:
            fb = firebase.create_firebase()
            existing = fb.database().child('tweets').shallow().get().val()

            for e in existing:
                if e not in terms:
                    print('DELETING OLD TREND >>> ', e)
                    fb.database().child('tweets').child(e).set(None)

        except Exception as e:
            print('FUCKED UP THE CLEAR ', e)

    for term in terms:
        if len(term) is 0:
            break

        try:
            thread = threading.Thread(target=TwitterSearch, args=(term, opts))
            thread.start()
        except Exception as e:
            print(e)
