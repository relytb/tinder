import fb_auth_token

# Rename this file fb_config.py after filling out the following values
fb_username = "your fb username here"
fb_password = "your fb password here"

fb_access_token = None
fb_user_id = None

def init():
    global fb_access_token
    if fb_access_token == None:
        fb_access_token = fb_auth_token.get_fb_access_token(fb_username, fb_password)
    global fb_user_id
    if fb_user_id == None:
        fb_user_id = fb_auth_token.get_fb_id(fb_access_token)