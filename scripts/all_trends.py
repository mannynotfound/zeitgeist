#!/usr/bin/env python3
import os
from subprocess import call
import argparse
from google_trends import search as google_search
from twitter_trends import search as twitter_search
from operator import itemgetter

def merge_trends(list1, list2):
    merge = {}

    def check_name(item):
        name = item['name'].lower()
        if merge.get(name, False):
            merge[name]['count'] += 1
        else:
            merge[name] = item

    for l in list1:
        check_name(l)

    for l2 in list2:
        check_name(l2)

    merged_list = list(map(lambda x: merge[x], merge))

    sorted_merge = sorted(merged_list, key=itemgetter('count'))
    sorted_merge.reverse()
    return sorted_merge


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-l', '--limit', type=int, help = 'max # of trends to search', default=10)
    ap.add_argument('-f', '--firebase', help = 'save data to firebase', action="store_true")
    args = vars(ap.parse_args())

    google_trends_to_search = google_search()['_result_json']
    twitter_trends_to_search = twitter_search()['_result_json']
    merged_trends = merge_trends(google_trends_to_search, twitter_trends_to_search)
    # reset master log
    open(os.path.normpath(os.getcwd()) + '/.master.log', 'w').close()

    print('TRENDS >>>> ')
    for idx, trend in enumerate(merged_trends):
        print('{0} | {1}'.format(idx, trend))

    for hot_trend in merged_trends[0:args['limit']]:
        realpath = os.path.normpath(os.getcwd()) + '/twitter_search.py'
        command = 'forever start --spinSleepTime 900000 -c python3 ' + realpath
        if args['firebase']:
            command += ' -f'

        command += ' -t'
        command_list = command.split()
        command_list.append('"' + hot_trend['name'] + '"')
        call(command_list)
