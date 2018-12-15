from api import getMatches
import sys
import os
from datetime import datetime

if __name__ == '__main__':
    matches = getMatches()
    for match in matches.values():
        if match['name'].lower() == sys.argv[2].lower() or match['_id'] == sys.argv[2]:
            print(match)