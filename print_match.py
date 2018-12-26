import os
import sys
from datetime import datetime

from api import getMatches

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
