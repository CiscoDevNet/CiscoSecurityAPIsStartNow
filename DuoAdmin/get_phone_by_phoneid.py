#!/usr/bin/env python

"""
For more information on this API, please visit:
https://duo.com/docs/adminapi

 -

Script Dependencies:
    requests

Depencency Installation:
    $ pip install -r requirements.txt

System Requirements:
    - Duo MFA, Duo Access or Duo Beyond account with aministrator priviliedges.
    - Duo Admin API enabled

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

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
# Get the phone id from the get_all_phones.py output
PHONE_ID = ''
API_PATH = '/admin/v1/phones/{}'.format(PHONE_ID)
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
    phone = requests.request(METHOD, url, headers=request_headers, verify=False)
    pprint.pprint(json.loads(phone.content))