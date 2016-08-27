#!/usr/bin/env python3
# code from https://github.com/pthrasher/sentiment/blob/master/sentiment.py

#
#  classifier.py
#  analyzes the sentiment of strings passed into stdin as json. (array of strings)
#
#  Created by Philip Thrasher on 2011-02-28.
#  Copyright 2011 pthrash entuhpryzizz. All rights reserved.
#
import os
import sys
import nltk.classify.util
import json
import pickle
import collections
import argparse
import io
import firebase

# load json
def load_json(path):
    try:
        with io.open(path, encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception as e:
        print('PROBLEM LOADING FILE', e)
        return []

# parse cli arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help = 'file to analyze')
ap.add_argument('-t', '--term', help = 'term to lookup in firebase')
ap.add_argument('-o', '--output', help = 'file to write results to')
ap.add_argument('-l', '--limit', type=int, help = 'file to analyze')
args = vars(ap.parse_args())

MIN_THRESHOLD = 0.37
MAX_THRESHOLD = 0.63
current_dir = os.path.dirname(os.path.realpath(__file__))
CLASSIFIER = current_dir + '/pickles/nbClassifier.pickle'
STOPWORDS = current_dir + '/pickles/stopwords.pickle'

class Classifier():
    def __init__(self):
        """docstring for __init__"""
        with open(CLASSIFIER, 'rb') as f:
            self.classifier = pickle.load(f)

    def _string_to_feature(self, text):
        """docstring for _string_to_feature"""
        words = text.split(" ")
        return dict([(word.lower(), True) for word in words])


    def _generate_features(self, strings):
        """generates the features for classification."""
        features = []
        for item in strings:
            print('generating features for ', item, ' ...')
            feature = self._string_to_feature(item)
            if not(MIN_THRESHOLD <= self.classifier.prob_classify(feature).prob('pos') <= MAX_THRESHOLD):
                features.append((feature, item,))
        return features

    def classify(self, strings):
        """docstring for analyze"""
        testsets = collections.defaultdict(set)
        features = self._generate_features(strings)
        for i, feature in enumerate(features):
            observed = self.classifier.classify(feature[0])
            testsets[observed].add(i)
        final = []
        for neg in testsets['neg']:
            final.append(dict(id=neg, content=features[int(neg)][1], classification='neg'))
        for pos in testsets['pos']:
            final.append(dict(id=pos, content=features[int(pos)][1], classification='pos'))
        return sorted(final, key=lambda d: int(d['id']))

if __name__ == '__main__':
    if args['file']:
        statuses = load_json(args['file'])
    elif args['term']:
        fb = firebase.create_firebase()
        statuses = fb.database().child('tweets').child(args['term']).get().val()
    else:
        print('PLEASE PROVIDE FILE OR TERM')
        sys.exit(1)

    print('GOT ', len(statuses), ' STATUSES')
    all_statuses = []
    for idx, status in enumerate(statuses):
        if args['limit'] is None or idx < args['limit']:
            all_statuses.append(status['text'])

    c = Classifier()
    results = c.classify(all_statuses)
    positive = [result for result in results if result['classification'] == 'pos']
    negative = [result for result in results if result['classification'] == 'neg']
    print("")
    for result in results:
        if result['classification'] == 'pos':
            print("Good: %s\n" % result['content'])
        else:
            print("Bad: %s\n" % result['content'])
    unknown = len(all_statuses) - len(results)

    out = "Statuses analyzed: %d | Positive: %d | Negative: %d | Unknown: %s" % (len(all_statuses), len(positive), len(negative), unknown)
    metrics = "Percentiles - Positive: %d%%, Negative: %d%%" % (float(len(positive))/float(len(results))*100, float(len(negative))/float(len(results))*100)

    print("="*84)
    print("= %s =" % out.center(80))
    print("= %s =" % metrics.center(80))
    print("="*84)
