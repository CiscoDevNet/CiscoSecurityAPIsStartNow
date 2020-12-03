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

# Get Applications from Tetration


def search_inventory(
        value,
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

    payload = {
        "filter": {
            "type": "eq",
            "field": "ip",
            "value": value
        }
}

    # HTTP Get Request
    response = restclient.post("/inventory/search", json_body=json.dumps(payload))

    # If response code is 200, then return the json response
    if response.status_code == 200:
        # JSON Response
        inventory = response.json()
        if inventory["results"]:
            return inventory
        else:
            print(f"\nERROR: IP Address {value} can not be found.")
            exit()

    # If response code is anything but 200, print error message with response code
    else:
        print(f"\nSomething went wrong. Error code {response.status_code}.")
        exit()

def get_app_scope(
        scope_id,
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
    response = restclient.get(f"/app_scopes/{scope_id}")

    # If response code is 200, then return the json response
    if response.status_code == 200:
        # JSON Response
        application_scope = response.json()

        return application_scope

    # If response code is anything but 200, print error message with response code
    else:
        print(f"Application Scope ID {scope_id} can not be found. Error code {response.status_code}.")

# If this script is the "main" script, run...

if __name__ == "__main__":

    # Search Inventory for IP Address

    ip = input("Enter the IP Address that you would like to Search Inventory: ")
    inventory = search_inventory(ip)
    # print(json.dumps(inventory, indent=4))
    hostname = inventory["results"][0]["host_name"]
    os = inventory["results"][0]["os"]
    os_version = inventory["results"][0]["os_version"]

    # Find Scope ID associated with inventory search
    if type(inventory["results"][0]["tags_scope_id"]) is str:
        app_scope_id = inventory["results"][0]["tags_scope_id"]
    else:
        app_scope_id = inventory["results"][0]["tags_scope_id"][-1]

    # Get Application Scope Details
    app_scope = get_app_scope(app_scope_id)
    # print(json.dumps(app_scope,indent=4))
    app_scope_name = app_scope["name"]
    print(f"\nIP address {ip} has been identified as hostname {hostname} running {os} {os_version} "
          f"\nfound in Application Scope {app_scope_name}.")

# End of File
