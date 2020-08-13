#!/usr/bin/python

import json, base64, email, hmac, hashlib, urllib3, urllib
import requests
import pprint
import config

# Disable SSL warnings
urllib3.disable_warnings()

# Imported API configuration variables
API_HOSTNAME = config.DUO_API_HOSTNAME
S_KEY = config.DUO_API_SECRET_KEY
I_KEY = config.DUO_API_INTEGRATION_KEY

# Script specific variables
METHOD = 'GET'
# Get the phone id from the get_all_users.py output
USER_ID = ''
API_PATH = '/admin/v1/users/{}'.format(USER_ID)
PARAMS = {}

# Request signing helper function
def sign(method=METHOD, 
         host=API_HOSTNAME, 
         path=API_PATH, 
         params=PARAMS, 
         skey=S_KEY, 
         ikey=I_KEY):

    """
    Return HTTP Basic Authentication ("Authorization" and "Date") headers.
    method, host, path: strings from request
    params: dict of request parameters
    skey: secret key
    ikey: integration key
    """

    # create canonical string
    now = email.utils.formatdate()
    canon = [now, method.upper(), host.lower(), path]
    args = []
    for key in sorted(params.keys()):
        val = params[key]
        if isinstance(val, str):
            val = val.encode("utf-8")
        args.append(
            '%s=%s' % (urllib.parse.quote(key, '~'), urllib.parse.quote(val, '~')))
    canon.append('&'.join(args))
    canon = '\n'.join(canon)
    print(canon)

    # sign canonical string
    sig = hmac.new(skey.encode('utf-8'), canon.encode('utf-8'), hashlib.sha1)
    auth = '%s:%s' % (ikey, sig.hexdigest())
    encoded_auth = base64.b64encode(auth.encode('utf-8'))

    # return headers
    return {'Date': now, 'Authorization': 'Basic %s' % str(encoded_auth, 'UTF-8')}

if __name__ == "__main__":

    url = "https://{}{}".format(API_HOSTNAME, API_PATH)
    request_headers = sign()
    user = requests.request(METHOD, url, headers=request_headers, verify=False)
    pprint.pprint(json.loads(user.content))