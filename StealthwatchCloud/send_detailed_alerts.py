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
from datetime import datetime
from datetime import timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#
import environment as env

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# FUNCTIONS

# Get Open Alerts from Stealthwatch Cloud


def get_swc_open_alerts(
        start_time,
        end_time,
    host=env.SWC.get("host"),
    api_key=env.SWC_API_KEY
):

    # Build URL
    url = f"https://{host}/api/v3/alerts/alert"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json','Authorization': api_key
}
    query_params = {"status": "open", "time__gte": start_time, "time__lt": end_time}

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
                              start_time,
                              end_time,
                          host=env.SWC.get("host"),
                          api_key=env.SWC_API_KEY
                          ):
    url = f"https://{host}/api/v3/observations/all"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json', 'Authorization': api_key
    }
    query_params = {"alert": alert_id, "time__gte": start_time, "time__lt": end_time}
    response = requests.get(url, headers=headers, params=query_params)
    response.raise_for_status()

    swc_obsv_alert = response.json()

    return swc_obsv_alert

def create_alert_message(alert_id, alert_type, alert_time, alert_url):
    split_text = alert_url.split("\n")
    url = split_text[1]

    alert_message = f"\nSecureX Cloud Analytics has triggered Alert {alert_id} - {alert_type}" \
        f" at {alert_time}. \nFor further details please go to {url}"

    return alert_message

def post_webex_teams_message(message,
                             host=env.WXT.get("host"),
                             api_key=env.WEBEX_TEAMS_ACCESS_TOKEN,
                             room_id=env.WEBEX_TEAMS_ROOM_ID
                             ):
    # Build URL
    url = f"https://{host}/v1/messages"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        "roomId": room_id,
        "text": message
    }
    json_payload = json.dumps(payload)

    # HTTP Get Request
    response = requests.post(url, headers=headers, data=json_payload)
    response.raise_for_status()

    # JSON Response
    post_res = response.json()

    return post_res

# If this script is the "main" script, run...


if __name__ == "__main__":

    # Set time variables
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    # Get SWC Open Alerts
    open_alerts = get_swc_open_alerts(start_time, end_time)
    # print(json.dumps(open_alerts, indent=4))

    # Query the total number of alerts
    swc_alert_count = open_alerts["meta"]["total_count"]
    # print(f"Alert!!! There are {swc_alert_count} total SecureX Cloud Analytics Alerts")

    # Array for all Alert Types
    swc_alert_table = []

    # If no Alerts exit send message and exit the script
    if swc_alert_count == 0:
        print(f"There are {swc_alert_count} alerts. Exiting the script")
        exit()
    # If there are Alerts, add alert info to swc_alert_table
    else:
        for alerts in open_alerts["objects"]:
            swc_alert_list = {}
            alert_id = alerts["id"]
            swc_alert_list.update({"alert_id": alert_id})
            alert_type = alerts["type"]
            swc_alert_list.update({"alert_type": alert_type})
            alert_time = alerts["time"]
            swc_alert_list.update({"alert_time": alert_time})
            alert_url = alerts["text"]
            swc_alert_list.update({"alert_url": alert_url})
            swc_alert_table.append(swc_alert_list)

    # print(json.dumps(swc_alert_table, indent=4))

    # Create Alert Messages for each
    for alert in swc_alert_table:
        alert_message = create_alert_message(alert["alert_id"],
                                                 alert["alert_type"],
                                                 alert["alert_time"],
                                                 alert["alert_url"])
        print(alert_message)

        # OPTIONAL - uncomment if testing Webex Teams integration
        # Send message to Webex Teams
        post_webex_teams_message(alert_message)


