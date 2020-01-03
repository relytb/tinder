import json
import os
import time
import requests

import fb_config

INSTA_URL = 'https://www.instagram.com/p/'
TINDER_URL = 'https://api.gotinder.com'
RECS_URI = '/v2/recs/core'
NOPE_URI = '/pass/{}'
LIKE_URI = '/like/{}'
AUTH_URI = '/v2/auth/login/facebook'
META_URI = '/meta'
UNMESSAGED_MATCHES_URI = '/v2/matches?count=100&is_tinder_u=false&locale=en&message=0'
MESSAGED_MATCHES_URI = '/v2/matches?count=100&is_tinder_u=false&locale=en&message=1'
LOCATION_URL = '/user/ping'
TOKEN_PATH = os.path.join(os.getcwd(), 'auth_token')

headers = {}

def getInstaPost(shortcode):
    request = requests.get(INSTA_URL + shortcode)
    html_text = request.text
    shared_data_index = html_text.index('window._sharedData')
    html_text = html_text[shared_data_index:]
    json_blob_start = html_text.index('{')
    json_blob_end = html_text.index('</script>') - 1
    json_blob = html_text[json_blob_start:json_blob_end]
    return json.loads(json_blob)['entry_data']

def _handleHttpError(retry):
    request = retry(headers)
    if request.status_code == 401:
        getAuthToken()
        request = retry(headers)
    request.raise_for_status()
    return request

def getAuthToken():
    if  os.path.exists(TOKEN_PATH):
        token_file = open(TOKEN_PATH)
        token = token_file.readlines()[0]
        token_file.close()
        headers['X-Auth-Token'] = token
        request = requests.get(TINDER_URL + META_URI, headers=headers)
        if request.status_code == 200:
            print('Loaded saved auth token')
            return

    print('No valid saved auth token, getting one manually')
    fb_config.init()
    req = requests.post(TINDER_URL + AUTH_URI, json={'token': fb_config.fb_access_token})
    tinder_auth_token = req.json()['data']['api_token']
    headers['X-Auth-Token'] = tinder_auth_token
    token_file = open(TOKEN_PATH, 'w')
    token_file.write(tinder_auth_token)
    token_file.close()
    print('You have been successfully authorized!')

def getMatches():
    matches = {}
    _getMatchesFromRequest(UNMESSAGED_MATCHES_URI, matches)
    _getMatchesFromRequest(MESSAGED_MATCHES_URI, matches)
    return matches

def _getMatchesFromRequest(uri, matches):
    request = _handleHttpError(lambda x: requests.get(TINDER_URL + uri, headers=x))
    json = request.json()
    for match in json['data']['matches']:
        matches[match['person']['_id']] = match['person']


def getRecs():
    request = _handleHttpError(lambda x: requests.get(TINDER_URL + RECS_URI, headers=x))
    json = request.json()
    if 'results' in json['data'].keys():
        return [profile['user'] for profile in json['data']['results'] if profile['type'] == 'user']
    else:
        return []

def spoofLocation(lat, lon):
    while True:
        print('Updating location to lat: {} lon: {}'.format(lat, lon))
        try:
            _handleHttpError(lambda x: requests.post(TINDER_URL + LOCATION_URL, json={'lat': lat, 'lon': lon}, headers=x))
        except Exception:
            # swallow
            print('swallow ping failure')
        time.sleep(60)

def like(profile):
    print('Swiping right on {}'.format(profile['name']))
    response = _handleHttpError(lambda x: requests.get(TINDER_URL + LIKE_URI.format(profile['_id']), headers=x))
    json = response.json()
    if 'rate_limited_until' in json.keys():
        return int(json['rate_limited_until']) / 1000

def nope(profile):
    print('Swiping left on {}'.format(profile['name']))
    _handleHttpError(lambda x: requests.get(TINDER_URL + NOPE_URI.format(profile['_id']), headers=x))
