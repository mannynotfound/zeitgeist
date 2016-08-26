#!/usr/bin/env python3
import lxml
import lxml.html as lh
import requests
from requests import Request, Session
from urllib.parse import quote, urlsplit
import os
from operator import itemgetter
from subprocess import call
import argparse
import sys

base_url = 'http://hawttrends.appspot.com/api/terms/'

def prepare_request(params):
    payload_str = "&".join("%s=%s" % (k,v) for k,v in params.items())
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/29.0.1547.65 Chrome/29.0.1547.65 Safari/537.36',
        'Accept-Encoding' : 'gzip, deflate, sdch, br'
        }
    cookie = {}
    req = Request('GET', base_url, params=payload_str, headers=headers, cookies=cookie)
    return req.prepare()

def execute_request(prepared_request, session=None):
    try:
        if session is None:
            session = Session()
        return session.send(prepared_request)
    except requests.exceptions.Timeout as e:
        raise

def sort_results(json):
    return sorted(list(map(int, json)))

def extract_results(json):
    trends = json['1']

    trend_counter = {}
    for trend in trends:
        if trend_counter.get(trend, False):
            trend_counter[trend] += 1
        else:
            trend_counter[trend] = 1

    def add_count(t):
        return {
                'name': t,
                'count': trend_counter[t]
                }

    trends_list = list(map(add_count, set(trends)))
    trends_filtered = sorted(trends_list, key=itemgetter('count'))
    trends_filtered.reverse()

    return trends_filtered

def search(params={}, session=None):
    # Prepare request
    request = prepare_request(params)

    # Execute Request
    result = execute_request(request, session)

    # Extract Results
    result_json = extract_results(result.json())

    # Return Result
    return {
        '_request': request,
        '_result': result,
        '_result_json': result_json,
        }

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-l', '--limit', type=int, help = 'max # of trends to search', default=10)
    ap.add_argument('-f', '--firebase', help = 'save data to firebase', action="store_true")
    args = vars(ap.parse_args())

    trends_to_search = search()['_result_json']
    for hot_trend in trends_to_search[0:args['limit']]:
        realpath = os.path.normpath(os.getcwd()) + '/twitter_search.py'
        command = 'forever start --spinSleepTime 900000 -c python3 ' + realpath
        if args['firebase']:
            command += ' -f'

        command += ' -t'
        command_list = command.split()
        command_list.append('"' + hot_trend['name'] + '"')
        call(command_list)
