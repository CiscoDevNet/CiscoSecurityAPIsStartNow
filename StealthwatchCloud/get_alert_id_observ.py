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


def get_swc_alert_observables(alert_id,
                          host=env.SWC.get("host"),
                          api_key=env.SWC_API_KEY
                          ):
    url = f"https://{host}/api/v3/observations/all"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json', 'Authorization': api_key
    }
    query_params = {"alert": alert_id}
    response = requests.get(url, headers=headers, params=query_params)
    response.raise_for_status()

    swc_obsv_alert = response.json()

    return swc_obsv_alert


# If this script is the "main" script, run...


if __name__ == "__main__":

    # Get SWC Open Alerts
    open_alerts = get_swc_open_alerts()
    # print(json.dumps(open_alerts, indent=4))

    # Query the total number of alerts
    swc_alert_count = open_alerts["meta"]["total_count"]
    print(f"Alert!!! There are {swc_alert_count} total SecureX Cloud Analytics Alerts")

    # Loop through all open alerts to find Inbound Port Scanner Observations
    for alerts in open_alerts["objects"]:
        if alerts['type'] == "Inbound Port Scanner":
            alert_id = alerts["id"]
            alert_id_observables = get_swc_alert_observables(alert_id)
            swc_observ_count = alert_id_observables["meta"]["total_count"]
            print(f"SecureX Cloud Analytics has found {swc_observ_count} External Port Scanner Observations "
                  f"as part of Inbound Port Scanner Alert ID {alert_id}.")
