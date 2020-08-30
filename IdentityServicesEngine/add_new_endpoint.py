import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"
endpoint_name = "PLC1"
endpoint_group = "7a4d98d0-ead9-11ea-a0f6-be6788d3bbfa"
endpoint_description = "Rockwell Automation PLC"
endpoint_mac = "00:11:22:33:44:55"

print(f"\n==> Add new user to ISE Internal Users group.")

if __name__ == "__main__":

    url = f"https://{hostname}:9060/ers/config/endpoint"

    payload = {"ERSEndPoint": {"name": endpoint_name, "description": endpoint_description,"mac": endpoint_mac,"groupId": endpoint_group}}

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, auth=(username,password), verify=False)

        if (response.status_code  == 201):
            print(f"User {endpoint_name} successfully added to group.")
        else:
            print(f"Error {response.status_code} returned from ISE.") 
    except:
        response.raise_for_status()

