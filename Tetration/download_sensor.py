#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python example script showing Cisco Secure Workload (Tetration).

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

import sys
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tetpyclient import RestClient

import environment as env

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#######################################################################
# Download agent
######################################################################
def download_agent(agent_options):

    # Ordered metadata used to construct the filename
    agent_metadata = [ { "option":None, "prefix":None, "suffix":None, "arch":None, "extension":None, "platform":None },
                       { "option":1, "prefix":"tet-win-sensor-", "suffix":".win64", "arch":"x86_64", "extension":".zip", "platform":"MSWindows10Pro" },
                       { "option":2, "prefix":"tet-sensor-", "suffix":".el5", "arch":"x86_64", "extension":".zip", "platform":"CentOS-5.11" },
                       { "option":3, "prefix":"tet-sensor-", "suffix":".el6", "arch":"x86_64", "extension":".zip", "platform":"CentOS-6.10" },
                       { "option":4, "prefix":"tet-sensor-", "suffix":".el7", "arch":"x86_64", "extension":".zip", "platform":"CentOS-7.8" },
                       { "option":5, "prefix":"tet-sensor-", "suffix":".el8", "arch":"x86_64", "extension":".zip", "platform":"CentOS-8.1" },
                       { "option":6, "prefix":"tet-sensor-", "suffix":".sles11", "arch":"x86_64", "extension":".zip", "platform":"SUSELinuxEnterpriseServer-11.4" },
                       { "option":7, "prefix":"tet-sensor-", "suffix":".sles11", "arch":"s390x", "extension":".zip", "platform":"SUSELinuxEnterpriseServer-11.4" },
                       { "option":8, "prefix":"tet-sensor-", "suffix":".sles12", "arch":"s390x", "extension":".zip", "platform":"SUSELinuxEnterpriseServer-12.5" },
                       { "option":9, "prefix":"tet-sensor-lw-", "suffix":".lw-linux-amd64", "arch":"amd64", "extension":".zip", "platform":"linux-amd64" },
                       { "option":10, "prefix":"tet-sensor-lw-", "suffix":".lw-linux-386", "arch":"386", "extension":".zip", "platform":"linux-amd64" },
                       { "option":11, "prefix":"tet-sensor-lw-", "suffix":".lw-aix-ppc", "arch":"ppc", "extension":".zip", "platform":"AIX-7.2" },
                       { "option":12, "prefix":"tet-sensor-lw-", "suffix":".lw-solaris-amd64", "arch":"amd64", "extension":".zip", "platform":"AIX-7.2" } ]

    platform_opt = agent_options["agent_platform"]
    agent_type = agent_options["agent_type"]

    agent_platform = agent_metadata[platform_opt]['platform']
    agent_arch = agent_metadata[platform_opt]['arch']

    agent_pkg_type = 'sensor_w_cfg'
    #agent_pkg_type = 'sensor_bin_pkg'

    host=env.TET.get("host")
    api_key=env.TET_API_KEY
    api_sec=env.TET_SEC

    # Build URL
    url = f"https://{host}"
 
    restclient = RestClient(url,
                            api_key=api_key,
                            api_secret=api_sec,
                            verify=True)

    print (" Getting supported agent version...")
    get_ver_url = "/sw_assets/download?platform=" + agent_platform + "&agent_type=" + agent_type + "&arch=" + agent_arch + "&list_version=True"
    response = restclient.get(get_ver_url)

    if response.status_code == 200:
        versions = response.content.decode('utf-8').splitlines()
        agent_version = versions[0].strip()
    else:
        print(f"Error {response.status_code} retrieving agent version.")
        sys.exit(1)

    # Now that we retrieved the supported version, we can form the complete filename
    agent_filename = agent_metadata[platform_opt]['prefix'] + agent_version + agent_metadata[platform_opt]['suffix'] + '.' + agent_arch + agent_metadata[platform_opt]['extension']

    # Now that we have the filename, we can create the download URL
    download_url = "/sw_assets/download?platform=" + agent_platform + "&agent_type=" + agent_type +"&pkg_type=" + agent_pkg_type + "&arch=" + agent_arch

    # Download agent
    print (" Downloading agent...")
    response = restclient.download(agent_filename, download_url)

    if not response.status_code == 200:
        print(f"Error code: {response.status_code} returned downloading agent.")
        sys.exit(1)

    print (" Agent download complete. Filename: "+ agent_filename )

#####################################################################
# Gracefully exit if user forgets to populate API credentials
#####################################################################
def check_API_creds ():
    if ( "tetration" in env.TET_API_KEY ):
        print("Error: Invalid API credentials. Check API keys in env.py")
        sys.exit(1)
 
#######################################################################
# Utility function to accept ranged numeric input or exit
######################################################################
def get_digit_input (minval, maxval, input_str):
    print(" Q)  QUIT/CANCEL \n")
    inp = input(input_str)
    if not inp.isdigit():
        # Assume q for any non-numeric and exit
        sys.exit()
    else:
        ret = int(inp)

    if (ret < minval or ret > maxval):
        print(f"Error: Input value outside of supported range")
        sys.exit(1)

    return ret

#######################################################################
# Get sensor token give app scope
######################################################################
def get_reg_token ():

    OUTPUT_TOKEN_FILE = 'registration.token'
    print ("")
    app_scope = input(" Enter application scope name for this agent to register with: ")

    host=env.TET.get("host")
    api_key=env.TET_API_KEY
    api_sec=env.TET_SEC

    # Build URL
    url = f"https://{host}"
 
    restclient = RestClient(url,
                            api_key=api_key,
                            api_secret=api_sec,
                            verify=True)

    resp = restclient.get('/secureconnector/name/{}/token'.format(app_scope))

    if resp.status_code != 200:
        print ("Error ({}): {}".format(resp.status_code, resp.content.decode()))
        sys.exit(1)
    else:
        with open(OUTPUT_TOKEN_FILE, 'w') as f:
            token_str=str(resp.content.decode())
            f.write(token_str)

    print (" Agent registration token retrieved. Filename: " + OUTPUT_TOKEN_FILE)


#######################################################################
# Prompt user to manually install/configure agent 
######################################################################
def prompt_config(agent_filename):
    print ("")
    print (" Follow these steps to complete the agent installation on Linux")
    print ("")
    print (" 1) Login as root and unzip "+agent_filename)
    print ("    For Linux agents, zip file will expand to following files:")
    print ("    sensor.cfg enforcer.cfg user.cfg tet-sensor*.rpm")
    print (" 2) Install the Linux RPM with this command:")
    print ("    # rpm -i tet-sensor-<ver>.<arch>.rpm'")
    print (" 3) The agent will automatically start after installation completes.")
    print ("    Stop the agent with command:")
    print ("    # systemctl stop tet-sensor")
    print (" 4) Copy the registration token & config files to the agent dir as follows: ")
    print ("    # install -m 644 enforcer.cfg /usr/local/tet/conf/enforcer.cfg")
    print ("    # install -m 644 sensor.cfg /usr/local/tet/conf/.sensor_config")
    print ("    # install -m 644 user.cfg /usr/local/tet/user.cfg")
    print ("    # install -m 644 registration.token /usr/local/tet/cert/registration.token")
    print (" 5) Get agent ACTIVATION_KEY from Tetration web UI and populate it")
    print ("    in /usr/local/tet/user.cfg as described in user guide:")
    print ("    https://<tet-host>/documentation/ui/software_agents/deployment.html")
    print (" 6) Start the agent with command:")
    print ("    # systemctl start tet-sensor")
 
#######################################################################
# Allow user to choose sensor platform/type/arch to download
######################################################################
def agent_chooser( ):

    print("\n Available Agent Platforms")
    print(" 1)  Windows (x86_64)")
    print(" 2)  CentOS or RedHat Linux 5.7 - 5.11 (x86_64)")
    print(" 3)  CentOS, RedHat or Oracle Linux 6.0 - 6.10 (x86_64)")
    print(" 4)  CentOS, RedHat or Oracle Linux 7.0 - 7.8 (x86_64)")
    print(" 5)  CentOS, RedHat or Oracle Linux 8.0 - 8.1 (x86_64)")
    print(" 6)  SUSE Linux 11.2 - 11.4 (x86_64)")
    print(" 7)  SUSE Linux 11.2 - 11.4 (s390x) ALPHA")
    print(" 8)  SUSE Linux 12.0 - 12.5 (s390x) ALPHA")
    print(" 9)  Universal Linux (amd64)")
    print(" 10) Universal Linux (386)")
    print(" 11) AIX (ppc)")
    print(" 12) Solaris (amd64)")
    platform_opt = get_digit_input(1, 12, " Choose Tetration agent platform to download (1-12): ")

    print("\n Available Agent Types")
    print(" 1)  Deep Visibility Agent")
    print(" 2)  Enforcement Agent")
    type_opt = get_digit_input(1, 2, " Choose agent type to download (1-2): ")

    if type_opt == 1:
        agent_opt = "sensor"
    else:
        agent_opt = "enforcer"

    options = { "agent_platform" : platform_opt,
                "agent_type" : agent_opt }

    return options
    
######################################################################
# MAIN
######################################################################
if __name__ == "__main__":

    check_API_creds

    # Prompt user to enter application scope and download registration token
    get_reg_token()

    # Allow user to choose agent options
    agent_options = agent_chooser()

    # Download agent
    download_agent(agent_options)

    print ("")
    print (" Agent package and registration token have been downloaded to")
    print (" this directory. Refer to agent deployment guide here for steps")
    print (" to install and configure the agent: ")
    print (" https://<tet-host>/documentation/ui/software_agents/deployment.html")
    print ("")
