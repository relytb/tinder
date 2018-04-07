import json
import os
import urllib.request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

PROFILE_NUMS = {'like': 0, 'nope': 0}
LIKE_DIR = "like"
NOPE_DIR = "nope"
INIT = False

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
    else:
        profile_folders = os.listdir(nope_path)
        print(profile_folders)
        PROFILE_NUMS[NOPE_DIR] = len(profile_folders)
        
    if not os.path.exists(like_path):
        os.makedirs(like_path)
    else:
        profile_folders = os.listdir(like_path)
        print(profile_folders)
        PROFILE_NUMS[LIKE_DIR] = len(profile_folders)

def _save_like(profile):
    _save_profile(profile, LIKE_DIR)

def _save_nope(profile):
    _save_profile(profile, NOPE_DIR)

def save_profile(profile):
    """ write profile to disc """
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
    for img_url in profile['pics']:
        img_path = os.path.join(profile_folder_path, "original_{}.jpg".format(pic_num))
        urllib.request.urlretrieve(img_url, img_path)
        pic_num += 1

    PROFILE_NUMS[swipe_dirname] += 1
