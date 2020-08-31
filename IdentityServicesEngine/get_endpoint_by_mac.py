import requests

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"
endpoint_mac = "00:11:22:33:44:55"

print(f"\n==> Returns the endpoint details for the requested MAC Address")

if __name__ == "__main__":

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    url = f"https://{hostname}:9060/ers/config/endpoint?filter=mac.EQ.{endpoint_mac}"

    try:
        response = requests.request("GET", url, headers= headers, auth=(username,password), verify=False)
    except:
        response.raise_for_status()

    endpoint_id = response.json()['SearchResult']['resources'][0]['id']
    endpoint_name = response.json()['SearchResult']['resources'][0]['name']
    
    print(f"Endpoint name is {endpoint_name} and ID is {endpoint_id}")
