import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"
new_user = "thomas"
new_pass = "C1sco12345"

print(f"\n==> Add new user to ISE Internal Users group.")

if __name__ == "__main__":

    url = f"https://{hostname}:9060/ers/config/internaluser"

    payload = {"InternalUser": {"name": new_user,"password": new_pass,"changePassword": "false"}}

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, auth=(username,password), verify=False)
        if (response.status_code  == 201):
            print(f"User {new_user} successfully added with password {new_pass}.")
        else:
            print(f"Error {response.status_code} returned from ISE.") 
    except:
        response.raise_for_status()

