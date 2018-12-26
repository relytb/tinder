from api import getMatches
import sys
import os
from datetime import datetime

if __name__ == '__main__':
    identifer = sys.argv[2]
    matches = getMatches()
    found = False
    for match in matches.values():
        if match['name'].lower() == identifer.lower() or match['_id'] == identifer:
            found = True
            print(match)

    if not found:
        print('Could not find match with identifier {}'.format(identifer))