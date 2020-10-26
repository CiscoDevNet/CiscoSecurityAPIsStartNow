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
from tetpyclient import RestClient

import environment as env

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# FUNCTIONS

# Test Connectivity to Tetration API


def tetration_test(
    host=env.TET.get("host"),
    api_key=env.TET_API_KEY,
        api_sec=env.TET_SEC
):

    # Build URL
    url = f"https://{host}"

    restclient = RestClient(url,
                            api_key=api_key,
                            api_secret=api_sec,
                            verify=True)

    # HTTP Get Request
    response = restclient.get("/applications")

    # If response code is 200, Test Successful
    if response.status_code == 200:
        print("Test Successful....Woo Hoo!")

        # return applications

    # If response code is anything but 200, print error message with response code
    else:
        print(f"Test Failed....DOE!"
              f"\nError Code {response.status_code}")


# If this script is the "main" script, run...

if __name__ == "__main__":

    # Run Test
    results = tetration_test()

