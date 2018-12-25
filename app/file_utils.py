import json
import os
import base64
import urllib.request
import threading

LIKE_DIR = 'like'
NOPE_DIR = 'nope'
BASE_DIR = 'C:\\Users\\Tyler\\tinder'

def _get_profile(request):
    profile = json.loads(request.body.decode('utf-8'))
    print('Got profile with keys {}'.format(profile.keys()))
    return profile

def _init_folders():
    nope_path = os.path.join(BASE_DIR, NOPE_DIR)
    like_path = os.path.join(BASE_DIR, LIKE_DIR)
    if not os.path.exists(nope_path):
        os.makedirs(nope_path)
        
    if not os.path.exists(like_path):
        os.makedirs(like_path)

def _save_like(profile):
    print('Saving like for {} ...'.format(profile['name']))
    _save_profile(profile, LIKE_DIR, BASE_DIR)

def _save_nope(profile):
    print('Saving nope {} ...'.format(profile['name']))
    _save_profile(profile, NOPE_DIR, BASE_DIR)

def save_profile(profile):
    write_call = None
    if profile['like'] == 1:
        write_call = lambda : _save_like(profile)
    else:
        write_call = lambda : _save_nope(profile)
    
    threading.Thread(target=write_call).start()

def _save_profile(profile, swipe_dirname, baseDir):
    profile_folder_path = os.path.join(baseDir, swipe_dirname)
    json_path = os.path.join(profile_folder_path, '{}_profile.json'.format(profile['_id']))
    with open(json_path, 'w') as profile_file:
        profile_file.write(json.dumps(profile))

    pic_num = 0
    for img_dict in profile['photos']:
        img_url = img_dict['url']
        print(img_url)
        img_path = os.path.join(profile_folder_path, '{}_{}.jpg'.format(profile['_id'], pic_num))
        try:
            urllib.request.urlretrieve(img_url, img_path)
        except urllib.error.HTTPError as err:
            print(err.code)
        pic_num += 1