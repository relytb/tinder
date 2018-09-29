from api import getMatches
import sys
import os
from datetime import datetime

if __name__ == '__main__':
    matches = getMatches(sys.argv[1])
    processed = set(id.split('_')[0] for id in (os.listdir('../like') + os.listdir('../nope') + os.listdir('../burned')))
    i = 0
    for match in matches.values():
        if match['_id'] not in processed:
            i += 1
            age = (datetime.now() - datetime.strptime(match['birth_date'], "%Y-%m-%dT%H:%M:%S.%fZ")).days // 365
            print('{} {} {}'.format(match['_id'], match['name'], age))
            for photo in match['photos']:
                print(photo['url'])
    print('Left to record: {} '.format(i))