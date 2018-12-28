import os
import shutil
import sys
import threading
import time
from multiprocessing import Pool
from random import shuffle

import requests

from api import getRecs, like, nope, spoofLocation
from constants import (DEBUG_MODE, NUM_CORES, SAMPLE_LIKES_DIR,
                       SAMPLE_NOPES_DIR, SAVED_LIKES_DIR, SAVED_NOPES_DIR,
                       TEMP_DIR, K)
from file_utils import _save_profile
from image_utils import run
from knn import knn, load

LIKES = {}
NOPES = {}

def setupDicts():
    nopes = load(SAMPLE_NOPES_DIR)
    nopes_keys = list(nopes.keys())
    shuffle(nopes_keys)
    for k in nopes_keys:
        NOPES[k] = nopes[k]
    print('{} nopes'.format(len(NOPES)))

    likes = load(SAMPLE_LIKES_DIR)
    likes_keys = list(likes.keys())
    shuffle(likes_keys)
    for k in likes_keys:
        LIKES[k] = likes[k]
    print('{} likes'.format(len(LIKES)))

if __name__ == '__main__':
    setupDicts()
    pool = Pool(processes=NUM_CORES)
    nope_count = 0
    like_count = 0
    if len(sys.argv) > 1:
            def target():
                spoofLocation(sys.argv[1], sys.argv[2])
            threading.Thread(target=target).start()
    while True:
        profiles = getRecs()
        if len(profiles) == 0:
            print('No one in your area. Going to sleep for a bit.')
            time.sleep(60*60)
        else:
            print('Got profiles')
        
        # call knn on each profile
        for profile in profiles:
            print('Saving {} {}'.format(profile['name'], profile['_id']))
            tmp_path = os.path.join(os.getcwd(), TEMP_DIR)
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)
            os.mkdir(tmp_path)
            _save_profile(profile, TEMP_DIR, os.getcwd())
            run(tmp_path, pool)
            profile_descriptors = load(tmp_path)
            swipes = []

            for profile_descriptor in profile_descriptors.keys():
                swipe = knn(K, profile_descriptors[profile_descriptor], LIKES, NOPES)
                swipes.append(swipe)
                print('Swiped {} on {}'.format('left' if swipe == 0 else 'right', profile_descriptor))
            
            profile['like'] = 1 if (len(swipes) > 0 and (sum(swipes)/len(swipes)) >= 0.5) or len(swipes) == 0 else 0
            
            if profile['like'] == 0:
                nope_count += 1
                if DEBUG_MODE:
                    print('Saving nope {} ...'.format(profile['name']))
                    for f in os.listdir(os.path.join(os.getcwd(), TEMP_DIR)):
                        if not os.path.exists(os.path.join(os.getcwd(), SAVED_NOPES_DIR, f)):
                            shutil.move(os.path.join(os.getcwd(), TEMP_DIR, f), os.path.join(os.getcwd(), SAVED_NOPES_DIR))
                else:
                    nope(profile)
                
            else:
                like_count += 1
                if DEBUG_MODE:
                    print('Saving like for {} ...'.format(profile['name']))
                    for f in os.listdir(os.path.join(os.getcwd(), TEMP_DIR)):
                        if not os.path.exists( os.path.join(os.getcwd(), SAVED_LIKES_DIR, f)):
                            shutil.move(os.path.join(os.getcwd(), TEMP_DIR, f), os.path.join(os.getcwd(), SAVED_LIKES_DIR))
                else:
                    like(profile)
            shutil.rmtree(tmp_path)
            print('Left: {}, Right: {} times'.format(nope_count, like_count))
