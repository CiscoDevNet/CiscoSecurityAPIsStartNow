import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"
endpoint_name = "IOT_Assets"
endpoint_description = "PLCs, HMIs, and other IOT Assets"

print(f"\n==> Creates a new endpoint group.")

if __name__ == "__main__":

    url = f"https://{hostname}:9060/ers/config/endpointgroup"

    payload = {"EndPointGroup" : {"name" : endpoint_name,"description" : endpoint_description}}

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, auth=(username,password), verify=False)
        endpoint_group = (response.headers["Location"][-36:])
        if (response.status_code  == 201):
            print(f"User {endpoint_name} successfully added Endpoint Group ID is {endpoint_group}")
        else:
            print(f"Error {response.status_code} returned from ISE.") 
    except:
        response.raise_for_status()

