from api import getMatches
import sys
import os
from datetime import datetime

if __name__ == '__main__':
    matches = getMatches()
    processed = set(path.split('_')[0] for path in (os.listdir('../like') + os.listdir('../nope') + os.listdir('../burned')))
    to_process = set(matches.keys()).difference(processed)

    i = 0
    for match_id in to_process:
        i += 1
        match = matches[match_id]
        age = (datetime.now() - datetime.strptime(match['birth_date'], "%Y-%m-%dT%H:%M:%S.%fZ")).days // 365
        print('{} {} {}'.format(match_id, match['name'], age))
        for photo in match['photos']:
            print(photo['url'])
    print('Left to record: {} '.format(i))