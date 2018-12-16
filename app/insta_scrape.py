import sys
import os
import json
from file_utils import save_profile
from image_utils import extract_id
from api import getInstaPost


def downloadProfile(shortcode):
    print('Getting profile for ' + shortcode)
    insta_post = getInstaPost(shortcode)
    if 'PostPage' in insta_post:
        profile = _convertInstaPostToProfile(insta_post)
        save_profile(profile)

def getSeen():
    entries = os.listdir('../like')
    return set([extract_id(entry) for entry in entries])

def sanitize(shortcode):
    return shortcode.replace('_', '')

def _convertInstaPostToProfile(insta_post):
    profile = {}
    profile['_id'] = sanitize(getShortcode(insta_post))
    profile['name'] = getName(insta_post)
    profile['like'] = 1
    
    photos = []
    pic_urls = getPicUrls(insta_post)
    for pic_url in pic_urls:
        photo = {}
        photo['url'] = pic_url
        photos.append(photo)
    profile['photos'] = photos
    return profile

def getPicUrls(insta_post):
    pic_urls = []
    shortcode_media = insta_post['PostPage'][0]['graphql']['shortcode_media']
    if 'edge_sidecar_to_children' in shortcode_media:
        # is photoset
        for edge in shortcode_media['edge_sidecar_to_children']['edges']:
            node = edge['node']
            if node['__typename'] == 'GraphImage':
                pic_urls.append(node['display_url'])
    else:
        # is single pic
        pic_urls.append(shortcode_media['display_url'])
    return pic_urls

def getName(insta_post):
    return insta_post['PostPage'][0]['graphql']['shortcode_media']['owner']['username']

def getShortcode(insta_post):
    return insta_post['PostPage'][0]['graphql']['shortcode_media']['shortcode']


if __name__ == '__main__':
    shortcodes_path = os.path.join(os.getcwd(), '../insta_likes')
    seen = getSeen()
    if os.path.exists(shortcodes_path):
        shortcodes_file = open(shortcodes_path)
        for shortcode in shortcodes_file.readlines():
            shortcode = shortcode.strip()
            if sanitize(shortcode) not in seen:
                downloadProfile(shortcode)
