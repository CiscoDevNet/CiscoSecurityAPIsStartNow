import requests

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

hostname = "198.18.133.27"
username = "admin"
password = "C1sco12345"

print(f"\n==> Returns a list of all administrative users.")

if __name__ == "__main__":

    headers = {
    'content-type': "application/json",
    'accept': "application/json"
    }

    url = f"https://{hostname}:9060/ers/config/adminuser"

    try:
        response = requests.request("GET", url, headers= headers, auth=(username,password), verify=False)
    except:
        response.raise_for_status()

    print(response.json())

