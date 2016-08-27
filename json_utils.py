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
    def convert_time(item):
        if item.get('unix_timestamp'):
            return item

        timestamp = item.get('created_at')
        if timestamp is None:
            item['unix_timestamp'] = 0
            return item
        else:
            item['unix_timestamp'] = time.mktime(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timetuple())
            return item

    items = list(map(lambda x: convert_time(x), data))
    sorted_data = sorted(items, key=itemgetter('unix_timestamp'))
    sorted_data.reverse()
    return sorted_data
