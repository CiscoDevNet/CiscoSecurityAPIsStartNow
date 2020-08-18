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

# Get Open Alerts from SecureX Cloud Analytics


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
    # print(start_time, end_time)

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
            source_name = alerts["source_name"]
            swc_alert_list.update({"source_name": source_name})
            swc_alert_table.append(swc_alert_list)

    # print(json.dumps(swc_alert_table, indent=4))

    # Loop through Alert Table and create action per Alert Type
    for alert_type in swc_alert_table:
        if alert_type["alert_type"] == "Inbound Port Scanner":
            port_scan_alert_id = alert_type["alert_id"]
            port_scan_alert_type = alert_type["alert_type"]
            split_text = alert_type["alert_url"].split("\n")
            port_scan_alert_url = split_text[1]

            port_scan_observ = get_swc_alert_observables(alert_type["alert_id"], start_time, end_time)
            # print(json.dumps(port_scan_observ, indent=4))

            for observ in port_scan_observ["objects"]:
                time = observ["time"]
                name = observ["observation_name"]
                scanner_ip = observ["scanner_ip"]
                scanned_ip = observ["scanned_ip"]

                port_scan_alert_message = f"\n SecureX Cloud Analytics has detected an {name} alarm on your network" \
                    f"\n where internal host(s) {scanned_ip} was scanned by external host(s) {scanner_ip} at {time}." \
                    f"\n Alert ID {port_scan_alert_id} - {port_scan_alert_type} has been generated" \
                    f"\n For additional information please go to {port_scan_alert_url}"

                print(port_scan_alert_message)

                # OPTIONAL - uncomment if testing Webex Teams integration
                # Send message to Webex Teams
                # post_webex_teams_message(port_scan_alert_message)

        elif alert_type["alert_type"] == "Excessive Access Attempts (External)":
            access_attempt_alert_id = alert_type["alert_id"]
            access_attempt_alert_type = alert_type["alert_type"]
            split_text = alert_type["alert_url"].split("\n")
            access_attempt_alert_url = split_text[1]
            access_attempt_time = alert_type["alert_time"]
            access_attempt_source_name = alert_type["source_name"]

            access_attempt_observ = get_swc_alert_observables(alert_type["alert_id"], start_time, end_time)
            # print(json.dumps(access_attempt_observ, indent=4))

            connected_ips = []

            for observ in access_attempt_observ["objects"]:
                connected_ip = observ["connected_ip"]
                connected_ips.append(connected_ip)

            # Set list to remove duplicates ip addresses
            attacker = []
            connected_ips_set = set(connected_ips)
            for ip in connected_ips_set:
                attacker.append(ip)

            # print(attacker)

            access_attempt_alert_message = f"\n SecureX Cloud Analytics has detected Multiple Access Failures" \
                f" targeted towards internal host {access_attempt_source_name} by attacker IP address(es) " \
                f"\n {attacker}. " \
                f"\n **Alert ID {access_attempt_alert_id} - {access_attempt_alert_type}** has been generated" \
                f"\n For additional information please go to " \
                f"\n {access_attempt_alert_url}"

            print(access_attempt_alert_message)

            # OPTIONAL - uncomment if testing Webex Teams integration
            # Send message to Webex Teams
            # post_webex_teams_message(access_attempt_alert_message)

        else:
            alert_message = create_alert_message(alert_type["alert_id"],
                                                 alert_type["alert_type"],
                                                 alert_type["alert_time"],
                                                 alert_type["alert_url"])
            print(alert_message)

            # OPTIONAL - uncomment if testing Webex Teams integration
            # Send message to Webex Teams
            # post_webex_teams_message(alert_message)

# End of File
