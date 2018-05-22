import os
import sys
import requests
import knn
import shutil
from views import _save_profile
from image_utils import run

TINDER_URL = 'https://api.gotinder.com/v2'
RECS_URL = '/recs/core'
NOPE_URL = '/pass/{}'
LIKE_URL = '/like/{}'
K = 5
TEMP_DIR = 'tmp'

def getRecs(xauthToken):
    headers = {'X-Auth-Token': xauthToken}
    json = requests.get(TINDER_URL + RECS_URL, headers=headers).json()
    return [profile['user'] for profile in json['data']['results'] if profile['type'] == 'user']

def like(profile):
    print('Swiping right on {}'.format(profile['name']))
    requests.get(TINDER_URL + LIKE_URL.format(profile['_id']))

def nope(profile):
    print('Swiping left on {}'.format(profile['name']))
    requests.get(TINDER_URL + NOPE_URL.format(profile['_id']))

if __name__ == '__main__':
    while True:
        # call update endpoint to load profiles into stack
        profiles = getRecs(sys.argv[1])
        print('Got profiles')
        # call knn on each profile
        for profile in profiles:
            print('Saving {}'.format(profile['_id']))
            tmp_path = os.path.join(os.getcwd(), os.pardir, TEMP_DIR)
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
            profile['like'] = sum(swipes)/len(swipes)
            
            shutil.rmtree(tmp_path)

            # Call endpoint to swipe left or right
            if profile['like'] == 0:
                nope(profile)
                print("Saving nope {} ...".format(profile['name']))
                _save_profile(profile, 'nope_swipe', os.path.join(os.getcwd(), os.pardir))
            else:
                like(profile)
                print("Saving like for {} ...".format(profile['name']))
                _save_profile(profile, 'like_swipe', os.path.join(os.getcwd(), os.pardir))

        
