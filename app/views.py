import json
import os
import base64
import urllib.request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

PROFILE_NUMS = {'like': 0, 'nope': 0}
LIKE_DIR = "like"
NOPE_DIR = "nope"

def save(request):
    """ save endpoint """
    _init_folders()
    save_profile(_get_profile(request))
    return HttpResponse("test")

def _get_profile(request):
    profile = json.loads(request.body.decode("utf-8"))
    print("Got profile with keys {}".format(profile.keys()))
    return profile


def _init_folders():
    nope_path = os.path.join(settings.BASE_DIR, NOPE_DIR)
    like_path = os.path.join(settings.BASE_DIR, LIKE_DIR)
    if not os.path.exists(nope_path):
        os.makedirs(nope_path)
    elif PROFILE_NUMS[NOPE_DIR] == 0:
        # initialize this
        profile_folders = os.listdir(nope_path)
        PROFILE_NUMS[NOPE_DIR] = len(profile_folders)
        
    if not os.path.exists(like_path):
        os.makedirs(like_path)
    elif PROFILE_NUMS[LIKE_DIR] == 0:
        profile_folders = os.listdir(like_path)
        PROFILE_NUMS[LIKE_DIR] = len(profile_folders)

def _save_like(profile):
    print("Saving like for {} ...".format(profile['name']))
    _save_profile(profile, LIKE_DIR)

def _save_nope(profile):
    print("Saving nope {} ...".format(profile['name']))
    _save_profile(profile, NOPE_DIR)

def save_profile(profile):
    """ write profile to disk """
    if profile['like'] == 0:
        _save_nope(profile)
    else:
        _save_like(profile)

def _save_profile(profile, swipe_dirname):
    profile_foldername = "profile_{}".format(PROFILE_NUMS[swipe_dirname])
    profile_folder_path = os.path.join(settings.BASE_DIR, swipe_dirname, profile_foldername)
    os.makedirs(profile_folder_path)
    json_path = os.path.join(profile_folder_path, "profile.json")
    with open(json_path, 'w') as profile_file:
        profile_file.write(json.dumps(profile))

    pic_num = 0
    for img_dict in profile['photos']:
        img_url = img_dict['url']
        print(img_url)
        img_path = os.path.join(profile_folder_path, "original_{}.jpg".format(pic_num))
        try:
            urllib.request.urlretrieve(img_url, img_path)
        except urllib.error.HTTPError as err:
            print(err.code)
        pic_num += 1

    PROFILE_NUMS[swipe_dirname] += 1
