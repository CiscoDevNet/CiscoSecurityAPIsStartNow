#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python example script showing Cisco Security Workload (Tetration).

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

# Search Inventory for IP address.

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

        return inventory

    # If response code is anything but 200, print error message with response code
    else:
        print(f"IP Address {value} can not be found. Error code {response.status_code}.")

# Search Application Scope assigned to IP address.

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

# Get all Applications.

def get_applications(
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

    # If response code is 200, then return the json response
    if response.status_code == 200:
        # JSON Response
        applications = response.json()

        return applications

    # If response code is anything but 200, print error message with response code
    else:
        print(f"Unable to find any Applications. Error code {response.status_code}.")

# Get detailed information of App ID.

def get_application_details(
        id,
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
    response = restclient.get(f"/applications/{id}/details")

    # If response code is 200, then return the json response
    if response.status_code == 200:
        # JSON Response
        app_detail = response.json()

        return app_detail

    # If response code is anything but 200, print error message with response code
    else:
        print(f"Unable to find Application ID {id}. Error code {response.status_code}.")

# If this script is the "main" script, run...

if __name__ == "__main__":

    # Search Inventory for IP Address
    ip = input("Enter the IP Address that you would like to Search Inventory: ")
    inventory = search_inventory(ip)
    # print(json.dumps(inventory, indent=4))
    hostname = inventory["results"][0]["host_name"]
    os = inventory["results"][0]["os"]
    os_version = inventory["results"][0]["os_version"]

    # Get the Application Scope ID
    scope_ids = []

    for scope in inventory["results"][0]["tags_scope_id"]:
        scope_ids.append(scope)

    # print(scope_ids)

    # Parse the most detailed App Scope ID
    app_scope_id = scope_ids[-1]
    # print(last_scope)

    # Get Application Scope Details
    app_scope = get_app_scope(app_scope_id)
    app_scope_name = app_scope["name"]

    # print(json.dumps(app_scope,indent=4))

    # Get all Application IDs
    applications = get_applications()
    # print(json.dumps(applications, indent=4))

    # Loop through Applications to find the App associated with defined App Scope

    for app in applications:
        if app["app_scope_id"] == app_scope_id:
            app_id = app["id"]
            # print(app_id)

            # Get details about Application Policies
            app_policy = get_application_details(app_id)
            # print(json.dumps(app_policy, indent=4))
            app_name = app_policy["name"]

            print(f"\nIP address {ip} has been identified as hostname {hostname} running {os} {os_version} "
                  f"\nfound in Application Scope {app_scope_name} and Application name {app_name}.")

# End of File
