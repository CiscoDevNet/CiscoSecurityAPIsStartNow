"""
This python module was created by Shubham Bharti.
Feel free to send comments/suggestions/improvements.  Either by email: shbharti@cisco.com or more importantly via a pull
request from the github repository: https://wwwin-github.cisco.com/shbharti/FMCAPI
"""


import requests
import json
import time
from requests.auth import HTTPBasicAuth
from getpass import getpass
import csv

# Function to convert a CSV to JSON
def csvtojson(csvFilePath):

    port = []
    icmpv4 = []
    icmpv6 = []



    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            if rows['type'] == "ProtocolPortObject":
                port.append(rows)
            if rows['type'] == "ICMPV4Object":
                icmpv4.append(rows)
            if rows['type'] == "ICMPV6Object":
                icmpv6.append(rows)

    # Delete the Key:Value pair of ICMP Type and Code for TCP/UDP Protocol Objects
    port_new = [{k: v for k, v in d.items() if k != "code" and k != "icmpType"} for d in port]

    # Delete the Key:Value pair of Protocol and Port for ICMP Objects
    icmpv4_new = [{k: v for k, v in d.items() if k != "protocol" and k != "port"} for d in icmpv4]

    # Delete the Key:Value pair of Protocol and Port for ICMP Objects
    icmpv6_new = [{k: v for k, v in d.items() if k != "protocol" and k != "port"} for d in icmpv6]


    return port_new, icmpv4_new, icmpv6_new

addr = input("Enter IP Address of the FMC: ")
username = input ("Enter Username: ")
password = getpass("Enter Password: ")

csvFilePath = input("Please enter the CSV Filepath (For eg. : path/to/file/objects.csv) :")

api_uri = "/api/fmc_platform/v1/auth/generatetoken"

url = "https://" + addr + api_uri
response = requests.post(url, verify=False, auth=HTTPBasicAuth(username, password))

accesstoken = response.headers["X-auth-access-token"]
refreshtoken = response.headers["X-auth-refresh-token"]
DOMAIN_UUID = response.headers["DOMAIN_UUID"]


port,icmpv4,icmpv6 = csvtojson(csvFilePath)

port_payload = json.dumps(port)
icmpv4_payload = json.dumps(icmpv4)
icmpv6_payload = json.dumps(icmpv6)

port_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/protocolportobjects?bulk=true"
icmpv4_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/icmpv4objects?bulk=true"
icmpv6_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/icmpv6objects?bulk=true"


port_url = "https://" + addr + port_api_uri
icmpv4_url = "https://" + addr + icmpv4_api_uri
icmpv6_url = "https://" + addr + icmpv6_api_uri

headers = {
  'Content-Type': 'application/json',
  'x-auth-access-token': accesstoken
}

if port != []:
    response = requests.request("POST", port_url, headers=headers, data = port_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("Port Objects successfully pushed")

    else:
        print("Port Object creation failed - Please check the log files for more detail")

    logfile = "log_"+ str(time.perf_counter_ns()) + ".txt"

    log = open(logfile,"w+")
    log.write(response.text)
    log.close

if icmpv4 != []:
    response = requests.request("POST", icmpv4_url, headers=headers, data = icmpv4_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("ICMPv4 Objects successfully pushed")

    else:
        print("ICMPv4 Object creation failed - Please check the log files for more detail")


    log = open(logfile,"a+")
    log.write(response.text)
    log.close

if icmpv6 != []:
    response = requests.request("POST", icmpv6_url, headers=headers, data = icmpv6_payload, verify = False)

    if response.status_code == 201 or response.status_code == 202:
        print("ICMPv6 Objects successfully pushed")

    else:
        print("ICMPv6 Object creation failed - Please check the log files for more detail")


    log = open(logfile,"a+")
    log.write(response.text)
    log.close

else :
    print("Please Validate that the CSV file provided is correct or at correct location")