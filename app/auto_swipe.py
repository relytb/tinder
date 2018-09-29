import os
import sys
import requests
import knn
import time
import threading
import shutil
from views import _save_profile
from image_utils import run
from api import getRecs, nope, like, spoofLocation
K = 5
TEMP_DIR = 'tmp'

if __name__ == '__main__':
    count = 0
    if len(sys.argv) > 2:
            def target():
                spoofLocation(sys.argv[1], sys.argv[2], sys.argv[3])
            threading.Thread(target=target).start()
    while True:
        # call update endpoint to load profiles into stack
        profiles = getRecs(sys.argv[1])
        print('Got profiles')
        # call knn on each profile
        for profile in profiles:
            print('Saving {}'.format(profile['_id']))
            tmp_path = os.path.join(os.getcwd(), os.pardir, TEMP_DIR)
            if os.path.exists(tmp_path):
                shutil.rmtree(tmp_path)
            os.mkdir(tmp_path)
            like_path = os.path.join(os.getcwd(), os.pardir, 'like_swipe')
            nope_path = os.path.join(os.getcwd(), os.pardir, 'nope_swipe')
            _save_profile(profile, TEMP_DIR, os.path.join(os.getcwd(), os.pardir))
            run(tmp_path)
            profile_descriptors = knn.load(tmp_path)
            swipes = []
            for profile_descriptor in profile_descriptors.keys():
                swipe = knn.knn(K, profile_descriptors[profile_descriptor])
                swipes.append(swipe)
                print('Swiped {} on {}'.format('left' if swipe == 0 else 'right', profile_descriptor))
            profile['like'] = 1 if (len(swipes) > 0 and (sum(swipes)/len(swipes)) >= 0.5) or len(swipes) == 0 else 0
            

            # Call endpoint to swipe left or right
            if profile['like'] == 0 and profile['name'] != 'Quinn':
                nope(sys.argv[1], profile)
                # print("Saving nope {} ...".format(profile['name']))
                # for f in os.listdir(os.path.join(os.getcwd(), os.pardir, TEMP_DIR)):
                #     if not os.path.exists( os.path.join(os.getcwd(), os.pardir, 'nope_swipe', f)):
                #         shutil.move(os.path.join(os.getcwd(), os.pardir, TEMP_DIR, f), os.path.join(os.getcwd(), os.pardir, 'nope_swipe'))
            else:
                like(sys.argv[1], profile)
                # print("Saving like for {} ...".format(profile['name']))
                # for f in os.listdir(os.path.join(os.getcwd(), os.pardir, TEMP_DIR)):
                #     if not os.path.exists( os.path.join(os.getcwd(), os.pardir, 'like_swipe', f)):
                #         shutil.move(os.path.join(os.getcwd(), os.pardir, TEMP_DIR, f), os.path.join(os.getcwd(), os.pardir, 'like_swipe'))
            
            shutil.rmtree(tmp_path)

        
