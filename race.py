#!/usr/bin/env python3
import curses
import math
import time
import json
import sys
import os
import io
import argparse
from TwitterWebsiteSearch import TwitterPager

# set up curses
def top_win(stdscr):
    (max_y, max_x) = stdscr.getmaxyx()
    begin_y = 0
    begin_x = 0
    height = int(math.ceil(max_y * .9))
    width = max_x
    top = curses.newwin(height, width, begin_y, begin_x)
    top.box() # adds border
    top.refresh()
    return top


def bottom_win(stdscr, top):
    (top_max_y, top_max_x) = top.getmaxyx()
    begin_y = top_max_y
    begin_x = 0
    height = (stdscr.getmaxyx())[0]
    width = top_max_x
    bottom = curses.newwin(height, width, begin_y, begin_x)
    bottom.box() # adds border
    bottom.refresh()
    return bottom


def top_stats(top, message):
    # write the stats to the top window
    top.addstr(1, 1, message)
    top.refresh()


def bottom_stats(bottom, message):
    # write the stats to the bottom window
    bottom.addstr(1, 1, message)
    bottom.refresh()


# parse cli arguments
ap = argparse.ArgumentParser()
ap.add_argument('-t', '--term', type=str, help = 'term to search for')
ap.add_argument('-l', '--limit', help = 'max amount of tweets to search for')

args = vars(ap.parse_args())
term = args['term']

if args['limit'] != None:
    limit = int(args['limit'])
else:
    limit = False

# create / load the directory
def load_json(path, filename):
    with io.open('{0}/{1}.json'.format(path, filename),
                 encoding='utf-8') as f:
        return json.loads(f.read())

def dump_json(path, term, data):
    with open(path + '/' + term + '.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f)

def perform_twitter_search(top, bottom, search_term):
    global limit
    # track our state
    total_count = 0
    print_count = 0
    all_tweets = []

    dump_path = os.path.dirname(os.path.realpath(__file__)) + '/dump'
    if not os.path.exists(dump_path):
        os.makedirs(dump_path)
    else:
        try:
            current_json = load_json(dump_path, search_term)
            if len(current_json) > 0:

                all_tweets = current_json
                print_count = len(current_json)

        except Exception as e:
            dump_json(dump_path, search_term, [])

    twitter_search_page = TwitterPager().get_iterator(search_term)
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
                    message = "{0} | {1}".format(print_count, tweet['text'])
                    top_stats(top, message)
                    bottom_stats(bottom, 'LOADING STATS....')

                    all_tweets.append(tweet)
                    if len(all_tweets) % 100 == 0:
                        try:
                            dump_json(dump_path, search_term, all_tweets)
                        except:
                            print('ERROR DUMPIN JSON')


def main(stdscr):
    # The start of the program
    # initialize windows
    global term
    top = top_win(stdscr)
    bottom = bottom_win(stdscr, top)
    perform_twitter_search(top, bottom, term)


if __name__ == '__main__':
    curses.wrapper(main)
