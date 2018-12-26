import os
import sys
from datetime import datetime

from api import getMatches
from constants import BURNED_DIR, SAMPLE_LIKES_DIR, SAMPLE_NOPES_DIR

if __name__ == '__main__':
    matches = getMatches()
    processed = set(path.split('_')[0] for path in (os.listdir(SAMPLE_LIKES_DIR) + os.listdir(SAMPLE_NOPES_DIR) + os.listdir(BURNED_DIR)))
    to_process = set(matches.keys()).difference(processed)

    i = 0
    for match_id in to_process:
        i += 1
        match = matches[match_id]
        age = (datetime.now() - datetime.strptime(match['birth_date'], '%Y-%m-%dT%H:%M:%S.%fZ')).days // 365
        print('{} {} {}'.format(match_id, match['name'], age))
        for photo in match['photos']:
            print(photo['url'])
    print('Left to record: {} '.format(i))
