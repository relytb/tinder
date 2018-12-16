import sys
import os
from api import getMatches
from file_utils import save_profile
from image_utils import run
from threading import Thread
import subprocess

if __name__ == '__main__':
    pic_id = sys.argv[2]
    is_like = int(sys.argv[1])
    match = getMatches()[pic_id]
    if is_like > 1:
        if not os.path.exists('../burned'):
            os.mkdir('../burned')
        open('../burned/' + match['_id'], 'a').close()
    else:
        match['like'] = is_like
        save_profile(match)
