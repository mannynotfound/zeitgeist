import io
import json
from operator import itemgetter
from datetime import datetime
import time

def load_json(path, filename):
    with io.open('{0}/{1}.json'.format(path, filename),
                 encoding='utf-8') as f:
        return json.loads(f.read())

def dump_json(path, term, data):
    with open(path + '/' + term + '.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f)

def sort_by_time(data):
    def convert_time(timestamp):
        return time.mktime(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timetuple())

    for item in data:
        item['unix_timestamp'] = convert_time(item['created_at'])

    sorted_data = sorted(data, key=itemgetter('unix_timestamp'))
    sorted_data.reverse()
    return sorted_data
