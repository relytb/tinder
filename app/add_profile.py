import sys
import os
from api import getMatches
from views import _save_like, _save_nope
from image_utils import run
from threading import Thread
import subprocess

if __name__ == '__main__':
    id = sys.argv[2]
    is_like = sys.argv[1]
    match = getMatches()[id]
    if is_like == '1':
        _save_like(match)
    elif is_like == '0':
        _save_nope(match)
    else:
        if not os.path.exists('../burned'):
            os.mkdir('../burned')
        open('../burned/' + match['_id'], 'a').close()
