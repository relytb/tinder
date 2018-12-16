import sys
import os
import urllib.request
import json
from views import _save_like
from image_utils import extract_id

INSTA_URL = "https://www.instagram.com/p/"

def downloadProfile(shortcode):
    print("Getting profile for " + shortcode)
    html_filepath = shortcode + ".html"
    urllib.request.urlretrieve(INSTA_URL + shortcode, html_filepath)
    shortcode_media = _getShortcodeMedia(html_filepath)
    if shortcode_media != None:
        profile = _convertToProfile(shortcode_media)
        _save_like(profile)

def getSeen():
    entries = os.listdir("../like")
    return set([extract_id(entry) for entry in entries])

def sanitize(shortcode):
    return shortcode.replace("_", "")

def _getShortcodeMedia(html_filepath):
    html_text = None
    with open(html_filepath, encoding="utf-8") as html_file:
        html_text = html_file.read()
        html_file.close()
        os.remove(html_filepath)
        shared_data_index = html_text.index("window._sharedData")
        html_text = html_text[shared_data_index:]
        json_blob_start = html_text.index('{')
        json_blob_end = html_text.index('</script>') - 1
        json_blob = html_text[json_blob_start:json_blob_end]
        entry_data = json.loads(json_blob)['entry_data']
        if 'PostPage' not in entry_data:
            print("Private profile, skipping")
            return None
        return entry_data['PostPage'][0]['graphql']['shortcode_media']

def _convertToProfile(shortcode_media):
    pic_urls = []
    if "edge_sidecar_to_children" in shortcode_media:
        # is photoset
        for edge in shortcode_media["edge_sidecar_to_children"]["edges"]:
            node = edge["node"]
            if node["__typename"] == "GraphImage":
                pic_urls.append(node["display_url"])
    else:
        # is single pic
        pic_urls.append(shortcode_media['display_url'])
    name = shortcode_media["owner"]["username"]
    shortcode = shortcode_media["shortcode"]
    profile = {}
    profile["_id"] = sanitize(shortcode)
    profile["name"] = name
    photos = []
    for pic_url in pic_urls:
        photo = {}
        photo["url"] = pic_url
        photos.append(photo)
    profile["photos"] = photos
    return profile


if __name__ == '__main__':
    shortcodes_path = os.path.join(os.getcwd(), sys.argv[1])
    seen = getSeen()
    if os.path.exists(shortcodes_path):
        shortcodes_file = open(shortcodes_path)
        for shortcode in shortcodes_file.readlines():
            shortcode = shortcode.strip()
            if sanitize(shortcode) not in seen:
                downloadProfile(shortcode)
    else:
        if sanitize(sys.argv[1]) not in seen:
            downloadProfile(sys.argv[1])
