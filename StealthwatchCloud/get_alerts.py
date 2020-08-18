#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python example script showing SecureX Cloud Analytics Alerts.

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


import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#
import environment as env

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# FUNCTIONS

# Get Open Alerts from Stealthwatch Cloud


def get_swc_open_alerts(
    host=env.SWC.get("host"),
    api_key=env.SWC_API_KEY
):

    # Build URL
    url = f"https://{host}/api/v3/alerts/alert"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json','Authorization': api_key
}
    query_params = {"status": "open"}

    # HTTP Get Request
    response = requests.get(url, headers=headers, params=query_params)

    # If response code is 200, then return the json response
    if response.status_code == 200:
        # JSON Response
        swc_alerts = response.json()

        return swc_alerts

    # If response code is anything but 200, print error message with response code
    else:
        print(f"An error has ocurred, while fetching alerts, with the following code {response.status_code}")

# If this script is the "main" script, run...


if __name__ == "__main__":

    # Get SWC Open Alerts
    open_alerts = get_swc_open_alerts()
    print(json.dumps(open_alerts, indent=4))

