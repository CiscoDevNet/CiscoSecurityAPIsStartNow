import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"
anc_policy = "Quarantine"
mac_address = "00:11:22:33:44:55"

print(f"\n==> Adds an endpoint to a quarantine ANC group")

if __name__ == "__main__":

    '''
    Leverages Adaptive Network Control on ISE to quarantine MAC address.
    '''

    url = f"https://{hostname}:9060/ers/config/ancendpoint/apply"
    
    payload = {"OperationAdditionalData": {"additionalData": [{"name": "macAddress","value": mac_address},{"name": "policyName","value": anc_policy}]}}

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    try:
        response = requests.request("PUT", url, data=json.dumps(payload), headers=headers, auth=(username,password), verify=False)
        if (response.status_code  == 204):
            print(f"MAC Address {mac_address} successfully added to {anc_policy} ANC policy.")
        else:
            print(f"Error {response.status_code} returned from ISE.") 
    except:
        response.raise_for_status()

