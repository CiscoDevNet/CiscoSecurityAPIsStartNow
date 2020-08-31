import requests
import xml.dom.minidom

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"
endpoint_group = "IOT_Assets"

print(f"\n==> Returns the Endpoint Group ID for the requested name")

if __name__ == "__main__":

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    url = f"https://{hostname}:9060/ers/config/endpointgroup?filter=name.EQ.{endpoint_group}"

    try:
        response = requests.request("GET", url, headers= headers, auth=(username,password), verify=False)
    except:
        response.raise_for_status()

    endpoint_group_id = response.json()['SearchResult']['resources'][0]['id']
    print(f"Endpoint Group ID for {endpoint_group} is {endpoint_group_id}")
