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
from file_utils import saveProfileWithProcessPool
from image_utils import run
from knn import knnWithProcessPool, runKnn, load, setupDicts


if __name__ == '__main__':
    pool = Pool(processes=NUM_CORES, initializer=setupDicts)
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
            time.sleep(10*60)
        else:
            print('Got profiles')
        
        # call knn on each profile
        for profile in profiles:
            print('Saving {} {}'.format(profile['name'], profile['_id']))
            tmp_path = os.path.join(os.getcwd(), TEMP_DIR)
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)
            os.mkdir(tmp_path)
            saveProfileWithProcessPool(profile, TEMP_DIR, os.getcwd(), pool)
            run(tmp_path, pool)
            profile_descriptors = load(tmp_path)

            swipes = runKnn(profile_descriptors, K, pool)
            print('Got swipes: {}, sum: {}'.format(swipes, sum(swipes)))      
            profile['like'] = 1 if sum(swipes) >= 0.4*len(swipes) else 0
            
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
