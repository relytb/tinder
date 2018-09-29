import requests

TINDER_URL = 'https://api.gotinder.com'
RECS_URI = '/v2/recs/core'
NOPE_URI = '/pass/{}'
LIKE_URI = '/like/{}'
UNMESSAGED_MATCHES_URI = '/v2/matches?count=100&is_tinder_u=false&locale=en&message=0'
MESSAGED_MATCHES_URI = '/v2/matches?count=100&is_tinder_u=false&locale=en&message=1'
LOCATION_URL = '/user/ping'

def getMatches(xauthToken):
    matches = {}
    _getMatchesFromRequest(xauthToken, UNMESSAGED_MATCHES_URI, matches)
    _getMatchesFromRequest(xauthToken, MESSAGED_MATCHES_URI, matches)
    return matches

def _getMatchesFromRequest(xauthToken, uri, matches):
    headers = {'X-Auth-Token': xauthToken}
    request = requests.get(TINDER_URL + uri, headers=headers)
    if request.status_code != 200:
        print("Status: {}, error: {}".format(request.status_code, request.text))
        raise Exception(request.text)
    json = request.json()
    for match in json['data']['matches']:
        matches[match['person']['_id']] = match['person']


def getRecs(xauthToken):
    headers = {'X-Auth-Token': xauthToken}
    r = requests.get(TINDER_URL + RECS_URL, headers=headers)
    if r.status_code != 200:
        print("Status: {}, error: {}".format(r.status_code, r.text))
        raise Exception(r.text)
    json = r.json()
    return [profile['user'] for profile in json['data']['results'] if profile['type'] == 'user']

def spoofLocation(xauthToken, lat, lon):
    headers = {'X-Auth-Token': xauthToken}
    while True:
        print('Updating location to lat: {} lon: {}'.format(lat, lon))
        try:
            requests.post(TINDER_URL + LOCATION_URL, json={"lat": lat, "lon": lon}, headers=headers)
        except Exception as e:
            # swallow
            print("swallow ping failure")
        time.sleep(60)

def like(xauthToken, profile):
    headers = {'X-Auth-Token': xauthToken}
    print('Swiping right on {}'.format(profile['name']))
    r = requests.get(TINDER_URL + LIKE_URL.format(profile['_id']), headers=headers)
    if r.status_code != 200:
        print("Status: {}, error: {}".format(r.status_code, r.text))
        raise Exception(r.text)

def nope(xauthToken, profile):
    headers = {'X-Auth-Token': xauthToken}
    print('Swiping left on {}'.format(profile['name']))
    r = requests.get(TINDER_URL + NOPE_URL.format(profile['_id']), headers=headers)
    if r.status_code != 200:
        print("Status: {}, error: {}".format(r.status_code, r.text))
        raise Exception(r.text)